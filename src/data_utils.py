import os
import json

def read_examples(data_dir, split_tag, data_num, world_size, local_rank, is_split=False):
# def read_examples(filename, data_num):
    """Read examples from filename."""
    examples = read_twinxsql(data_dir, split_tag)
    return examples

def read_twinxsql(data_dir, split_tag):
    examples = []
    if split_tag == 'train':
        filename = os.path.join(data_dir, f"train.json")
    elif split_tag == 'test':
        filename = os.path.join(data_dir, f"test.json")
    else:
        filename = os.path.join(data_dir, f"valid.json")
    with open(filename) as f:
        for idx, line in enumerate(f):
            x = json.loads(line)
            resultMmap = (" <s> " +  x["resultMmap_2"][0]) if len(x["resultMmap_2"])>0 else ""
            sqlFragment = (" <s> " + x["sqlFragment_2"][0]) if len(x["sqlFragment_2"])>0 else ""
            examples.append(
                Example(
                    idx=idx,
                    source= x["comm_2_en"].strip()+ " <s> " + x["comm_1_en"].strip() + " <s> " + ' '.join(x["code_1"].replace("\n"," ").replace("\t"," ").strip().split(" ")) + resultMmap + sqlFragment,
                    target= ' '.join(x["code_2"].replace("\n"," ").replace("\t"," ").strip().split(" ")),
                    old_code=' '.join(x["code_1"].replace("\n"," ").replace("\t"," ").strip().split(" "))
                )
            )
            idx += 1
    return examples

class Example(object):
    """A single training/test example."""

    def __init__(self,
                 idx,
                 source,
                 target,
                 old_comm='',
                 old_code='',
                 new_comm='',
                 new_code=''
                 ):
        self.idx = idx
        self.source = source
        self.target = target
        self.old_comm = old_comm
        self.old_code = old_code
        self.new_comm = new_comm
        self.new_code = new_code

class InputFeatures(object):
    """A single training/test features for a example."""

    def __init__(self,
                 example_id,
                 source_ids,
                 target_ids,
                 url=None
                 ):
        self.example_id = example_id
        self.source_ids = source_ids
        self.target_ids = target_ids

def convert_examples_to_features(item):
    example, example_index, tokenizer, args, stage = item
    if args.add_task_prefix:
        source_str = "{}: {}".format(args.task, example.source)
    else:
        source_str = example.source
    source_str = source_str.replace('</s>', '<unk>')
    source_ids = tokenizer.encode(source_str, max_length=args.max_source_len, padding='max_length', truncation=True)
    assert source_ids.count(tokenizer.eos_token_id) == 1
    if stage == 'test':
        target_ids = []
    else:
        target_str = example.target
        target_str = target_str.replace('</s>', '<unk>')
        target_ids = tokenizer.encode(target_str, max_length=args.max_target_len, padding='max_length',
                                      truncation=True)
        assert target_ids.count(tokenizer.eos_token_id) == 1

    return InputFeatures(
        example_index,
        source_ids,
        target_ids,
    )