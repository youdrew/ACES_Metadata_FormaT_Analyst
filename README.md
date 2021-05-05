# ACES_Metadata_Format_Analyst
[ACES](https://acescentral.com/) Metadata Format Analysis tool GUI. A tool for color artist who use .amf file.

Related Projects：

[`amf-util`](https://github.com/pomfort/amf-util)

[`amf-implementation`](https://github.com/dtatut/amf-implementation)

[`aces-dev`](https://github.com/ampas/aces-dev/tree/master)
&nbsp; 

&nbsp; 

&nbsp; 


## ACES's background knowledge
[ACES](https://acescentral.com/) is a global standard for interchanging digital image files, managing color workflows and creating masters for delivery and archiving.

It is a combination of [SMPTE](https://www.smpte.org/) standards, best practices, and sophisticated color science developed by hundreds of professional filmmakers and color scientists under the auspices of the Science and Technology Council of the [Academy of Motion Picture Arts and Sciences](https://www.oscars.org/).

[ACES](https://acescentral.com/) can be used on any type of production from features to television, commercials, AR/VR and more.
&nbsp; 

&nbsp; 

&nbsp; 



## ACES Metadata Format's background knowledge
[ACES](https://acescentral.com/) does not specify [ACES](https://acescentral.com/)‘s configuration points directly or associate them with actual imagesor shots during production, and this is the very reason why AMF exists.

AMF is the configuration file that allows a precise setup for an [ACES](https://acescentral.com/) engine. Besides this basicgoal, AMF is also the tool of choice to transmit and exchange configuration parameters in orderto ensure consistency within a workflow and across the entire ecosystem of tools that are usedwithin that workflow.

AMF is an XML specification that describes the configuration of an [ACES](https://acescentral.com/) color pipeline together with the various input transforms, look transforms and output transforms.AMF is a "sidecar' element that accompanies some visual material such as a video file or a sequence of frames or a whole composition (i.e timeline). In the case of a composition, more than one AMF file can be used if the composition requires different configurations of the [ACES](https://acescentral.com/) pipeline. It is also worth mentioning that several AMF files can reference the same visual material.

If you are an artist, you can download [**AMF Handbook**](https://community.acescentral.com/uploads/short-url/35NJKAucKujBY9g2lZjr1gNwk20.pdf).

If you are a developer, you can download [**S-2019-001**](https://community.acescentral.com/uploads/short-url/e4v6I9CuoMv5wauxqwnUkLvWjw6.pdf).

for more infomation.
&nbsp; 

&nbsp; 

&nbsp; 




## ACES Metadata Format Analyst 
ACES Metadata Format Analyst is an open source project designed for color artists. We want to create a simple AMF analysis and processing GUI tool, with lightweight, and run on Mac and Win systems.

It has the following functions **under development**:

+ Analyze the content of the AMF file and display in a tabular, highly readable manner.

+ Batch import and process AMF files.

+ Input an AMF file and render a result in the way of ACES color pipeline.

+ Display LMT information in the form of Cube and Cruve.

+ Output AMF file information in various forms(i.e EXCEL, CUBE LUT etc).
