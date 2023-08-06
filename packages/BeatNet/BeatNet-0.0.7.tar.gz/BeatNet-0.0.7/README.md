# BeatNet
A package for music online and offline rhythmic information analysis including music Beat, downbeat, tempo and meter tracking.

[![PyPI](https://img.shields.io/pypi/v/BeatNet.svg)](https://pypi.org/project/BeatNet/)
[![CC BY 4.0][cc-by-shield]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-beat-tracking-on-gtzan)](https://paperswithcode.com/sota/online-beat-tracking-on-gtzan?p=beatnet-crnn-and-particle-filtering-for)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-downbeat-tracking-on-gtzan)](https://paperswithcode.com/sota/online-downbeat-tracking-on-gtzan?p=beatnet-crnn-and-particle-filtering-for)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-beat-tracking-on-ballroom)](https://paperswithcode.com/sota/online-beat-tracking-on-ballroom?p=beatnet-crnn-and-particle-filtering-for)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-downbeat-tracking-on-ballroom)](https://paperswithcode.com/sota/online-downbeat-tracking-on-ballroom?p=beatnet-crnn-and-particle-filtering-for)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-beat-tracking-on-rock-corpus)](https://paperswithcode.com/sota/online-beat-tracking-on-rock-corpus?p=beatnet-crnn-and-particle-filtering-for)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/beatnet-crnn-and-particle-filtering-for/online-downbeat-tracking-on-rock-corpus)](https://paperswithcode.com/sota/online-downbeat-tracking-on-rock-corpus?p=beatnet-crnn-and-particle-filtering-for)



This repository contains the user package and the source code of the Monte Carlo particle flitering inference model of the "BeatNet" music online joint beat/downbeat/tempo/meter tracking system. The arxiv version of the original ISMIR-2021 paper: 

*[arXiv 2108.03576](https://arxiv.org/abs/2108.03576)*

In addition to the proposed online inference, we added madmom's DBN beat/downbeat inference model for the offline usages. Note that, the offline model still utilize BeatNet's neural network rather than that of Madmom which leads to better performance and significantly faster results.

Note: All models are trained using ***pytorch*** and are included in the models folder. In order to recieve the training script and the datasets data/feature handlers, shoot me an email at mheydari [at] ur.rochester.edu     

System Input:
-------------
Raw audio waveform 

System Output:
--------------
A vector including beats and downbeats columns, respectively with the following shape: numpy_array(num_beats, 2).

Installation command:
---------------------
Approach #1: Installing binaries from the pypi website:
```
pip install BeatNet
```

Approach #2: Installing directly from the Git repository:
```
pip install git+https://github.com/mjhydri/BeatNet
```
Usage example:
--------------
```
From BeatNet.BeatNet import BeatNet

estimator = BeatNet(1) 

Output = estimator.process("music file directory", inference_model= 'PF', plot = True)
```  
A brief video tutorial of the system (Overview):
------------------------------------------

[![Easy song](https://img.youtube.com/vi/xOX74cXQKrY/0.jpg)](https://youtu.be/xOX74cXQKrY)

___________________________________________________________________

  
In order to demonstrate the performance of the system for different beat/donbeat tracking difficulties, here are three video demo examples :

1: Song Difficulty: Easy
  
  
[![Easy song](https://img.youtube.com/vi/XsdA4AATaUY/0.jpg)](https://www.youtube.com/watch?v=XsdA4AATaUY)
  



2: Song difficulty: Medium
  
  [![Easy song](https://img.youtube.com/vi/GuW8C5xuWbQ/0.jpg)](https://www.youtube.com/watch?v=GuW8C5xuWbQ)
  




3: Song difficulty: Veteran
  
  [![Easy song](https://img.youtube.com/vi/dFbFGMs9CA4/0.jpg)](https://www.youtube.com/watch?v=dFbFGMs9CA4)
  

Acknowledgements:
-----------------
For the input feature extraction and implementing of the beat state space,  [Librosa](https://github.com/librosa/librosa) and [Madmom](https://github.com/CPJKU/madmom) libraries are ustilzed. Many thanks for their great jobs. This work has been partially supported by the National Science Foundation grants 1846184 and DGE-1922591.

References:
-----------

M.  Heydari,  F.  Cwitkowitz,  and  Z.  Duan,    “BeatNet:CRNN and particle filtering for online joint beat down-beat and meter tracking,” in Proc. of the 22th Intl. 
Conf.on Music Information Retrieval (ISMIR), 2021.

M. Heydari and Z. Duan, “Don’t Look Back: An online beat  tracking  method  using  RNN  and  enhanced  particle filtering,”  in Proc. IEEE Int. Conf. Acoust. Speech Signal Process. (ICASSP), 2021.

