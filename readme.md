
# Introduction

The repository for Paper "Specific-Component Aware Pretraining for XML Code Updating"

![xml](./assets/xml.png)

The above figure shows an XML-formatted file containing multiple XML code blocks. The code block in lines 30-62 is used to query information of `GreenParkEvaluationDTO` , while the code block in lines 100-132 is used to query information of `IndustryInfoDTO`. For better presentation, we utilize different color to highlight the changed content and place the code fragments referenced by these two queries above their respective locations~(i.e., with the code starting from line 10 and line 20). These two XML's query code have similar functionalities and structures, and such similar scenarios may appear many times within the same file.
**In this scenario, referencing existing XML code and automatically updating the target XML code has become a intuitive way for improving the efficiency of XML code development**. 



![pre-training](./assets/pre-training.png)

To enable the model to capture domain-specific information, we design the specific component-aware denoising~(SCAD) framework. This framework is tailored to incorporate the unique data characteristics of a particular domain into the pre-training process, thereby bolstering the model's capacity to adapt to that specific domain. As depicted in the upper part of above figure, the main idea behind SCAD is to set pre-training tasks~(e.g., $T_1$, $T_2$, and so on) based on different components of the data and design additional pre-training tasks~(e.g., $T_{link\ 1,2}$) that connect these different components.
Specifically, in each task~(e.g., $T_1$), denoising strategies are applied only to a particular component~(i.e. $SC_1$), and each denoising is designed based on the characteristics of the current component.

In the TwinXSQL dataset, focusing on code updating tasks, XML code encompasses specific structure and value. Consequently, we design three distinct pre-training tasks tailored for XML structures, values, and there links, respectively, aiming to acquire domain-specific knowledge pertinent to XML code. 
The lower part of figure illustrates the basic idea of these three pre-training tasks.


![resutls](./assets/results.png)
The above table illustrates a comparative analysis of experimental results between XSQLT5 and generic code models. Notably, when holding the similar parameter scale, models fine-tuned on XML-specific pre-trained models consistently outperform those fine-tuned on generic code models. 

# Dataset
You can find the TwinXSQL dataset from `/data/TwinXSQL`.

# Models
You can find the model with fine-tuned weights from [release](https://github.com/LIANGQINGYUAN/SCAD-TwinXSQL/releases/tag/model).

# Fine-tuning
You can find the fine-tuning details from `/src`.
