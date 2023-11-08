# Automating Attendance System using Face Recognition with Masks
Due to Covid-19 and its variants, many people have been contaminated and died in Mauritius. While the island's financial sector is fragile after a three-month lockdown, another lockdown can result in an economic crisis. With the risk of contamination higher in environments such as offices, I decided to find a solution that will help as prevention against Covid-19. 

The attendance system at RT Knits is archaic and requires a person to swipe his card on an electronic device. Seeing that we can automate the system to avoid contact with potentially contaminated persons, I propose a face recognition system. While this system already exists and is an old system, I realized we would need a ```Face Recognition with Masks ```.

A mask on the face significantly increases the difficulty of finding a solution. After months of failing, I successfully designed the automated attendance system using face recognition with masks. With the number of deaths due to Covid-19 increasing each day, any precautionary measure not taken can be a question of life and death.

## Abstract
```Face detection``` is an old concept, ```face verification``` can be done by a 9-year old and ```face recognition``` now requires only a dozen lines of code. In this project, I want to explore the possibility of ```Face recognition``` while wearing a ```mask```. When wearing a mask, a person's face is hidden by 60-70%. Using only 30-40% of a person's face, I designed a ```face mask recognition``` model with an accuracy of ```99.84%```. Trained on a modified CASIA dataset containing images with and without masks, the model could successfully get the embeddings of ```85743``` people within 5 min and perform perfect face recognition with and without masks.


## Dataset(s)
1. CASIA-Webface Dataset to train our model: https://drive.google.com/uc?id=1Of_EVz-yHV7QVWQGihYfvtny9Ne8qXVz&export=download
- dataset contains ```494,414``` images of ```10,575``` people. This dataset does not provide any bounding boxes for faces or any other annotations.

2. LFW Dataset for evaluation of Face Recognition **without** Masks: http://vis-www.cs.umass.edu/lfw/
- dataset contains more than ```13,233``` images of faces collected from the web of ```5,749``` people. Each face has been labeled with the name of the person pictured. ```1,680``` of the people pictured have two or more distinct photos in the data set.

3. 1% of the MS-Celeb-1M dataset for evaluation of Face Recognition **with** Masks: https://academictorrents.com/details/9e67eb7cc23c9417f39778a8e06cca5e26196a97/tech&hit=1&filelist=1
- dataset has ```8,456,240``` images of ```99,892``` celebrities. 	

## Action Plan
Being a long and complex project I divided it into three phases:

 - **Phase 1:** We will discuss the theoretical and mathematical concept that lies behind face detection, verification, and recognition.
 - **Phase 2:** Using the concepts discussed, we will perform various image processing techniques on our dataset to clean our data for better accuracy.
 - **Phase 3**: We will train our model from scratch to perform face mask recognition.

The most important part of this project remains the data collection and data cleaning process. Using a ```data-centric``` approach, we will systematically enhance our dataset to improve accuracy and prevent overfitting by performing ```Data Augmentation``` and ```Stratified Sampling``` and keeping our model architecture constant.

Many of the concepts explained below have been inspired by ```Andrew Ng's``` Deep Learning Specialization course. After numerous research to explain AI and CNN concepts in the simplest way possible, Andrew Ng's material remains by far the most insightful I encountered. 

## Phase 1: Face Recognition Concept

### 1.1 Face Verification vs Face Recognition

### 1.1.1 Verification - Is this the same person?
Face verification is quite simple. We can take our FaceID for example which we use to unlock our phone or at the airport when scanning our passport and verifying if it is really us. So it works in 2 steps:

- **We input the image or the ID of a person.**
- **We verify if the output is the same as the claimed person.**

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142724385-df2203a3-5f8c-435f-8ea6-7f9cc690861a.png" />
  </p>

It is a ```1:1``` problem. We expect to have a high accuracy of the face verification system - ```>99%``` - so that it can further be used into the face recognition system.

### 1.1.2 Face Recognition - Who is this person?
Face recognition is much harder than face verification. It is used mainly for attendance system in offices, or when facebook automatically tags your friend. The process is as such:

- **We have a database of K persons.**
- **We take the image of a person.**
- **We output the ID if the image is any of the K persons or if it is not.**

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142724421-6f94ee75-3731-493b-86d7-3b0836847b80.png" />
 </p>

Face recognition is a ```1:K``` problem where K is the number of persons in our database.

### 1.2 The One Shot Learning Dilemma
The problem with the face recognition for automating the attendance system at RT Knits is to be able for the neural network to recognize a particular person from only **one** image. Since we are going to have only one picture of the employees, the system should be able to recognize the person again. 

Suppose we have 100 employees then one simple solution would be to take this one image and feed it into a CNN and output a softmax unit with 101 outputs(100 outputs is for the employees and the one left is to indicate none). However, this would not work well for two reasons:

1. We will have a very little training set hence, we will not be able to train a robust neural network.
2. Suppose we have another employee joining in then we would have to increment our outputs and re-train our Conv-Net. 

Instead, we would want our neural network to learn a ```similarity function.```

### 1.3 Similarity Function

The similarity function takes as input two images and output the degree of difference between the two images - <img src="https://latex.codecogs.com/svg.image?d(img_{1},&space;img_{2})" title="d(img_{1}, img_{2})" />

- For two images of the **same** person, we want <img src="https://latex.codecogs.com/svg.image?d(img_{1},&space;img_{2})" title="d(img_{1}, img_{2})" /> to be small.
- For two images of **different** persons, we want <img src="https://latex.codecogs.com/svg.image?d(img_{1},&space;img_{2})" title="d(img_{1}, img_{2})" /> to be big.


So how do we address the face verification problem?
- If <img src="https://latex.codecogs.com/svg.image?d(img_{1},&space;img_{2})&space;\leq&space;\tau&space;" title="d(img_{1}, img_{2}) \leq \tau " />, we predict as ```same```.
- If <img src="https://latex.codecogs.com/svg.image?d(img_{1},&space;img_{2})&space;>&space;&space;\tau&space;" title="d(img_{1}, img_{2}) > \tau " />, we predict as ```different```.

where <img src="https://latex.codecogs.com/svg.image?\tau&space;" title="\tau " /> is a threshold.

Given a new image, we use that function ```d``` to compare against the images in our database. If the image pairs are different then we would have a large number and if they are the same then we would have a small enough number that will be less than our ```threshold``` <img src="https://latex.codecogs.com/svg.image?\tau&space;" title="\tau " />.

![image](https://user-images.githubusercontent.com/59663734/142725497-32e644cd-0562-40ab-a569-46e57108918e.png)

For someone not in our database, when we will do the pairwise comparison and compute the function ```d``` then we would expect to get very large numbers for all the pairs as shown above. The ```d``` function solves the ```one shot learning``` problem whereby if someone new joins the team then we only need to add that new person's image to our database and it would work just fine. 

### 1.4 Siamese Network
The idea of running two identical convolutional neural networks on two different inputs and comparing them is called a Siamese Neural Network. 

We feed in a picture of a person into a sequence of convolutions, pooling and fully connected layers and end up with a 128 feature vector. These 128 numbers is represented by <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;f(x^{(i)})" title="f(x^{(i)})" /> and is called the ```encoding or embedding``` of the image where <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;img_{(i)}&space;=&space;x^{(i)}" title="img_{(i)} = x^{(i)}" />.

![image](https://user-images.githubusercontent.com/59663734/142727867-2fa4f25e-3768-4c64-849b-6f4d5fe0e16d.png)

The to build a face recognition system would be to have a second picture feed in into that same CNN and compare their two 128 feature vectors. Then we need to define the function ```d``` which computes the norm of the difference of the two encodings:

![CodeCogsEqn (6)](https://user-images.githubusercontent.com/59663734/142728088-50968b17-3545-40af-84cb-071bfa9598eb.png)

To sum up: 
- our neural network define a **128-dimensional encoding** <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;f(x^{(i)})" title="f(x^{(i)})" /> of an image. 
- we want to learn parameters such that the if two pictures are the **same** then the distance of the two encodings should be **small**.
- In contrast, for two **different** images, we want that distance to be **large**. 

When we vary the parameters of the different layers of our NN, we end up with different encodings. But we want to learn a specific set of parameters such that the above two conditions are met.

### 1.5 Embedding
In order to understand what is a face ```embedding``` or ```encoding```, we should first ask ourselves how do we recognise a face? The method which requires the least mental effort would be to remember the distinct facial characteristics of an individual. Color of the eyes, long nose, large ears, color of the skin, scars, and so one are all distinct features which we look in a person if we want to remember them after looking at them only once. In this way, we expect our NN to do the same thing.

Using  a vector of 128 numbers, our AI will try to compress all the necessary features of a face into this space.  Mapping high-dimensional data (like images) into this low-dimensional representations (embeddings) is what will allow us to give each face an ```ID```. As such, embeddings of similar faces are similar - a person can have only one ID.

#### 1.5.1 Content of an Embedding
So what do the numbers in the embedding vector mean? Size of the eyes? Distance between the nose and the eyes? Mouth width? The answer is simply: **we don't really know!** We don’t directly tell our NN what the numbers in the vector should represent during training, we only require that the embedding vectors of similar faces are also similar (i.e. close to each other). It’s up to our NN to figure out how to represent faces with vectors so that the vectors of the same people are similar and the vectors of different people are not. For this to be true, our NN needs to identify **key features** of a person’s face which separate it from different faces. Our NN is trying out many different combinations of these features during training until it finds the **ones** that work the best. Our neural network don’t represent features in an image the same way as we do (distance, size, etc.) and it is better this way as this enable it to do a far better job than us humans.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143775596-261ee8dd-8ac2-4672-9458-efbe82ca56fe.png" />
</p>
<p align="center">   Fig. A function which takes an image as the input and outputs the face embedding (a summary of the face).</p>

What we would want in our case is the NN to generate embeddings such that it is nearly the same for a person with and without masks. In this way our model will be able to predict the correct person even with a mask.

This process of training a convolutional neural network to output face embeddings requires a lot of data and computer power. It took me about ```46 hours``` of continuous training to get good accuracy. But once the network has been trained, it can generate measurements for any face, even ones it has never seen before! So this step only needs to be done once.

#### 1.5.2 How to know the correct embedding dimension?
FaceNet experimented with different embedding dimensionalities and ```128``` remains the best performing one. In this project my embedding length will be a constant 128 feature vector.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143775364-7bdd3baf-bc5f-4b57-b3b5-040618d89bc2.png" />
</p>


### 1.6 Triplet Loss Function
In Triplet Loss, we will be looking at three images at a time: an ```anchor```, a ```positive``` image(one who is similar to the anchor image) and a ```negative``` image(one who is different from the anchor image). We want the distance between the anchor and the positive to be minimum and the distance between the anchor and the negative image to be maximum. 

We denote the ```anchor``` as ```A```, ```positive``` as ```P``` and ```negative``` as ```N```. 

For a robust face recognition, we want the following:

<img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\left\|f(A)-f(P)&space;\right\|^2\leq&space;\left\|f(A)-f(N)&space;\right\|^2" title="\left\|f(A)-f(P) \right\|^2\leq \left\|f(A)-f(N) \right\|^2" /> where <img src="https://latex.codecogs.com/svg.image?d(A,P)&space;=&space;\left\|f(A)-f(P)&space;\right\|^2" title="d(A,P) = \left\|f(A)-f(P) \right\|^2" /> and <img src="https://latex.codecogs.com/svg.image?d(A,N)&space;=&space;\left\|f(A)-f(N)&space;\right\|^2" title="d(A,N) = \left\|f(A)-f(N) \right\|^2" />

We can also write the equation above as :

<img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\left\|f(A)-f(P)&space;\right\|^2&space;-&space;&space;\left\|f(A)-f(N)&space;\right\|^2\leq&space;0" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2\leq 0" />

To make sure the neural network does not output zero for all the encodings, i.e, it does not set all the encodings equal to each other, we modify the above equation such that the difference between ```d(A,P)``` and ```d(A,N)``` should be <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;0-\alpha&space;" title="0-\alpha " /> where <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\alpha&space;" title="\alpha " /> is called a ```margin```

Finally, the equation becomes:

<img src="https://latex.codecogs.com/svg.image?\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha&space;&space;\leq&space;0" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha \leq 0" />

For example, if we have d(A,N) = 0.50 and d(A,P) = 0.49, then the two values are too close to each other and it is not good enough. We would want d(A,N) to be much bigger than d(A,P) like 0.7 instead of 0.50. To achive this gap of 0.2, we introduce the margin <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\alpha&space;" title="\alpha " /> which helps push d(A,N) up or push d(A,P) down to achieve better results. 

To define our loss fucntion on a single triplet we need 3 images: ```A```, ```P``` and ```N```:

<img src="https://latex.codecogs.com/svg.image?L(A,P,N)&space;=&space;max(\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha,&space;0)" title="L(A,P,N) = max(\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha, 0)" />

- we take the ```max``` of the loss because as long as <img src="https://latex.codecogs.com/svg.image?\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha" /> <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\leq&space;" title="\leq " /> 0, the loss = 0.
-  However if <img src="https://latex.codecogs.com/svg.image?\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha" /> > 0 then the loss = <img src="https://latex.codecogs.com/svg.image?\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha" />. We will have a ```positive``` loss.

To define our ```cost function```:
<img src="https://latex.codecogs.com/png.image?\dpi{100}&space;J&space;=&space;\sum_{i=1}^{m}&space;=&space;L(A^{(i)},P^{(i)},N^{(i)})" title="J = \sum_{i=1}^{m} = L(A^{(i)},P^{(i)},N^{(i)})" />

**Note**: We need atleast more than 1 picture of a person as we need a pair of ```A``` and ```P``` in order to train our NN.

![image](https://user-images.githubusercontent.com/59663734/142739186-12eab359-fe42-458f-99cd-662dbba9a34e.png)
<p align="center">
  Fig. The anchor(in orange) pulls images of the same person closer and pushes images of a different person further away.
  </p>

To summarise:

1. We randomly select an ```anchor``` image(orange border).
2. We randomly select  an image of the same person as the anchor image - ```positive```(green border).
3. We randomly select  an image of a different person as the anchor image - ```negative```(red border).
4. We train our model and adjust parameters so that the positive image is closest to the anchor and the negative one is far from the anchor. 
5. We repeat the process above so that all images of the same person are close to each other and further from the others.

The diagram above shows the steps described.

**Note:** One of the problem when we choose A,P and N randomly is that the conditon <img src="https://latex.codecogs.com/svg.image?\left\|f(A)-f(P)&space;\right\|^2&space;-&space;\left\|f(A)-f(N)&space;\right\|^2&space;&plus;&space;\alpha&space;\leq&space;&space;0" title="\left\|f(A)-f(P) \right\|^2 - \left\|f(A)-f(N) \right\|^2 + \alpha \leq 0" /> is easily satisfied and the NN will not learn much from it. What we want is to choose triplets that are **hard** to train on. That is in order to satisfy this condition: <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;d(A,P)&space;&plus;&space;\alpha&space;\leq&space;d(A,N)" title="d(A,P) + \alpha \leq d(A,N)" />, we want <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;d(A,P)&space;\approx&space;d(A,N)" title="d(A,P) \approx d(A,N)" />. Now the NN will try hard to push d(A,N) and push d(A,P) up so that there is atleast a margin <img src="https://latex.codecogs.com/png.image?\dpi{100}&space;\alpha&space;" title="\alpha " /> between the two components. Thus, it is important to understand that it is only by choosing hard triplets that our gradient descent will really do some learning of the similarity and differences in the images. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143772056-e2609c88-29e0-48ae-bfa8-100bf99e6061.png" />
</p>
<p align="center"> Fig. They are not twins. One of them is Will Ferrell and the other is Chad smith. </p>

After training our AI, it will recognise a person on an unseen image by calculating its embedding and use this embedding to calculate the distances to images of known people. If the face embedding is close enough to embeddings of person A(Rowan Atkinson), we say that this image contains the face of person A.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143081544-1d3ad257-328d-459d-bc03-b6c194bfc6af.png" />
</p>

At RT Knits we have 2000 employees and we assume we will have 20,000 images(10 pictures of each employee), then we need need to take these 20K pictures and generate triplets of ```(A,P,N)``` and then train our learning algorithm by using gradient descent to minimize the cost function defined above. This will have the effect of backpropagating to all the parameters in the NN in order to learn an encoding such that <img src="https://latex.codecogs.com/svg.image?d(x^{(i)},x^{(j)})" title="d(x^{(i)},x^{(j)})" /> is small for images of the same person and big for images of different person. 

### 1.7 Face Verification with Binary Classification
Another option to the Triplet Loss Function is to to take the Siamese Network and have them compute the 128-dimensional embedding to be then fed to a logistic regression unit to make prediction.

- Same person: <img src="https://latex.codecogs.com/svg.image?\hat{y}&space;=&space;1" title="\hat{y} = 1" />
- Different person: <img src="https://latex.codecogs.com/svg.image?\hat{y}&space;=&space;0" title="\hat{y} = 0" />

The output <img src="https://latex.codecogs.com/svg.image?\hat{y}" title="\hat{y}" /> will be a ```sigmoid function``` applied to the difference between the two sets of encodings. The formula below computes the element-wise difference in absolute values between the two encodings:

<img src="https://latex.codecogs.com/svg.image?\hat{y}&space;=&space;\sigma&space;(\sum_{k=1}^{128}w_{i}\left|f(x^{(i)})_{k}&space;-&space;f(x^{(j)})_{k}&space;\right|&space;&plus;&space;b&space;)" title="\hat{y} = \sigma (\sum_{k=1}^{128}w_{i}\left|f(x^{(i)})_{k} - f(x^{(j)})_{k} \right| + b )" />

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142739837-07e261de-9201-4eb4-857e-1c532f6138da.png" />
</p>

In summary, we just need to create a training set of pairs of images where ```target label = 1``` of **same** person and ```target label = 0``` of **different** person.

## Phase 2: Data Processing
![2-Figure1-1](https://user-images.githubusercontent.com/59663734/142723133-243c6b53-47ea-43e7-809b-c4dd790aa98f.png)

### 2.1 Face Detection with SSD
Object detection refers to the task of identifying various objects within an image and drawing a bounding box around each of them. Initially, researchers developed R-CNN for object detection, localization, and classification. The output is a bounding box surrounding the object detected with the classification result of the object. With time, we improved the R-CNN network and came up with Fast R-CNN and Faster R-CNN. However, one major drawback of the network was that the inference time was too long for real-time object detection. New architectures such as ```YOLO``` and the ones described below are better suited for real-time object detection.

There are several methods for face detection:
- SSD
- MTCNN
- Dlib
- OpenCV

Our goal is to use a face detection algorithm to detect faces and crop it with margin 20 or 40 as shown below. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142823899-d1193e71-a01a-4844-9810-6185488384d5.png" />
</p>

While MTCNN is more widely used, SSD performs faster inference however has low accuracy. SSD uses lower resolution layers to detect larger scale objects. It speeds up the process by eliminating the need for the region proposal network.

The architecture of SSD consists of 3 main components:

1. Base network - VGG-16
2. Extra feature layers
3. Prediction layers

Before we dive in into SSD, it is important we understand our Object Localisation and Object Detection works.

**1. How does it work?**

By starting simple, suppose we want to perform object localisation whereby if we detect a person's face in a picture we want to know where in the picture is the face located. We may also have other objects in the picture, for example a car, we will also need to take this into consideration. Now our CNN softmax output will not just contain the object class label but also the parameters below:

![CodeCogsEqn](https://user-images.githubusercontent.com/59663734/142835042-35a3de01-1d18-4d8b-9c7f-e3d12080960d.png) where

- p: "0" if no object and "1" if object
- c1: "1" if face, "0" otherwise
- c2: "1" if car, "0" otherwise
- x: x-position - center point of object
- y: y-position - center point of object
- w: width of bounding box
- h: height of bounding box
 
If we have a picture as shown below we may divide it into a ```5x5``` grid cells and predict what value will our ```y``` predict in each individual cell.

![image](https://user-images.githubusercontent.com/59663734/142837554-05605efa-da36-480f-a710-f013153da318.png)

For the first grid cell which does not contain an object, we have p = 0 as the first parameter in our ```y``` value and for the rest, we don't care so we use ```?``` to represent them. For the third grid cell, we detect an object and a face so out p = 1 and c1 = 1, and the x,y,w and h represent values for the bounding box. During training, we will try to make our network output similar vectors. 

SSD does not use a pre-defined region proposal network. Instead, it computes both the location and class scores using small convolution filters. After extracting the feature maps, SSD applies 3 × 3 convolution filters for each cell to make predictions.

**2. How to know our bounding box is correct?**

```IoU``` is used to measure the overlap between two bounding boxes. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142840525-4db003b6-9a6a-4b08-9ee7-8002216cdc2b.png" />
</p>

Normally if our IoU is greater than or equal to 0.5 we deem it to be a correct prediction. But we can be more stringent and increase the threshold where 1 is the maximum value.

**3. Anchor Boxes**
1. It is not possible for one object to be strictly within one grid cell. And when it is not, how do we determine which cell do we associate to the object.  
- The solution for this is to associate the cell which contains the **center point** of the bounding box of the object. 

2. Each of the grid cells can detect only one object. But we may have one grid cell containing more than one object. How do we handle multiple center points?
- We can use a bigger grid - 19x19 - instead of a 5x5 which reduces this problem. Also, we need to do is predefined anchor boxes and associate prediction with the anchor boxes. 

Previously, each object is assigned to a grid cell that contains that object's midpoint. Now, each object is assigned to a grid cell which contains that object's midpoint **and** anchor box for the grid cell with the highest IoU(similar shape).  

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142845336-85efa649-4611-47d9-8885-f8660a13ad8f.png" />
</p>

For the image above, both objects have their counterpoint in the same cell. So we set a tall anchor box that can be used to predict a standing person and a wide anchor box can be used to predict a car. We use these anchor boxes in each of the grid cell and output one vector y for every anchor box. 

**4. Non-Maximal Suppression (NMS)**

SSD contains 8732 default boxes. During inference, we have 8732 boxes for each class (because we output a confidence score for each box). Most of these boxes are negative and among the positive ones, there would be a lot of overlapping boxes.  Non-Maximal Suppression (NMS) is applied to get rid of overlapping boxes per class. It works as such: 

1. sort the boxes based on the confidence score
2. pick the box with the largest confidence score
3. remove all the other predicted boxes with Jaccard overlap > the NMS threshold (0.45 here)
4. repeat the process until all boxes are covered.

![image](https://user-images.githubusercontent.com/59663734/142847066-bb095fbe-e264-4029-a348-f04fdabd2978.png)

To sum up:
- The network is very sensitive to default boxes and it is important to choose the default boxes based on the dataset that it is being used on.
- SSD does not work well with small objects: earlier layers which have smaller receptive fields and are responsible for small object detection, are too shallow. 

**5. Implementation**

I used a trained facemask detection algorithm to crop the pictures. Similar to the one explained above, I adjusted the bounding box to crop the images:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142854038-95faeefb-a400-4c99-ba09-b92d44424c7b.png" />
</p>

I loaded the ```.pb``` file with a default margin of 44 and GPU-ration of 0.1:

```
    def __init__(self,pb_path,margin=44,GPU_ratio=0.1):
        # ----var
        node_dict = {'input': 'data_1:0',
                     'detection_bboxes': 'loc_branch_concat_1/concat:0',
                     'detection_scores': 'cls_branch_concat_1/concat:0'}
```

We restore the model to get the nodes and get the input shape which is used to resize the images:

```
        # ====model restore from pb file
        sess, tf_dict = model_restore_from_pb(pb_path, node_dict,GPU_ratio = GPU_ratio)
        tf_input = tf_dict['input']
        model_shape = tf_input.shape  # [N,H,W,C]
        print("model_shape = ", model_shape)
        img_size = (tf_input.shape[2].value,tf_input.shape[1].value)
        detection_bboxes = tf_dict['detection_bboxes']
        detection_scores = tf_dict['detection_scores']
```

In the ```inference``` function we use sess.run to get the detection boxes, the detection scores:

```
        y_bboxes_output, y_cls_output = self.sess.run([self.detection_bboxes, self.detection_scores],
                                                      feed_dict={self.tf_input: img_4d})
```

We then need to decode the bounding boxes and do the non-max suppression:

```
        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = self.decode_bbox(self.anchors_exp, y_bboxes_output)[0]
        y_cls = y_cls_output[0]
        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        keep_idxs = self.single_class_non_max_suppression(y_bboxes, bbox_max_scores,  conf_thresh=self.conf_thresh,
                                                          iou_thresh=self.iou_thresh )
        # ====draw bounding box
```

In order to draw the bounding box we need to get the (xmin,ymin) and (xmax,ymax) coordinates. Our bounding boxes are unit coordinates in the range [0,1]. We have to make them to real sizes. We need to get the width of the bounding box using (xmax-xmin) and height using (ymax-ymin).

```
        # ====draw bounding box
        for idx in keep_idxs:
            conf = float(bbox_max_scores[idx])
            #print("conf = ",conf)
            class_id = bbox_max_score_classes[idx]
            bbox = y_bboxes[idx]
            #print(bbox)

            xmin = np.maximum(0, int(bbox[0] * ori_width - self.margin / 2))
            ymin = np.maximum(0, int(bbox[1] * ori_height - self.margin / 2))
            xmax = np.minimum(int(bbox[2] * ori_width + self.margin / 2), ori_width)
            ymax = np.minimum(int(bbox[3] * ori_height + self.margin / 2), ori_height)

            re_boxes.append([xmin, ymin, xmax - xmin, ymax - ymin])
            re_confidence.append(conf)
            re_classes.append('face')
            re_mask_id.append(class_id)
        return re_boxes, re_confidence, re_classes, re_mask_id
```

Our original image is 250x250 so we want our cropped face image to be over 100x100. This enables us to detect faces which is well aligned(the main person in the image). We use two thresholds for the width and height:

```
    width_threshold = 100 + margin // 2 #allow us to get a full face and not cropped ones
    height_threshold = 100 + margin // 2
```

In an ```if``` condition we check if the width of our bbox is more than the width_threshold and the height is more than the height_threshold then the height of the cropped image  is ```bbox[1]:bbox[1] + bbox[3]``` and width is ```bbox[0]:bbox[0] + bbox[2]```. We then save the file. 

```
            for num,bbox in enumerate(bboxes):
                if bbox[2] > width_threshold and bbox[3] > height_threshold:
                    img_crop = img_ori[bbox[1]:bbox[1] + bbox[3],bbox[0]:bbox[0] + bbox[2], :]
                    save_path = os.path.join(save_dir,str(idx) + '_' + str(num) + ".png")
                    # print("save_path:",save_path)
                    cv2.imwrite(save_path,img_crop)
```

We display the images:

![image](https://user-images.githubusercontent.com/59663734/142858127-52759a18-4b40-4447-9426-1cc8fe851f50.png)


### 2.2 Data Cleaning
After cropping the pictures, we check the folders and we see that in folder ```0000157``` we got one mislabelled image as shown below. This signifies that the CASIA dataset is not a cleaned dataset and there may be other instances of mislabelled images. We cannot check each of the ```10,575``` folders individually so we need an algorithm that will do this for us. 

![image](https://user-images.githubusercontent.com/59663734/142935195-d12ee28e-7dc3-4f2f-8b91-538c3919e5fb.png)

We can set a process of removing mislabelled images using the distance function ```d``` described before:

1. In a subfolder in the main directory, we select one image one by one as the **target image** and the other images become the **reference images**.
2. We calculate the average distances between the target image and the reference image. 
3. We see that the average distance, when a correct image is selected as the target image, is not much as compared to when the mislabelled image is selected as the target image. Also, we might have more than one mislabelled image in a folder. That is the reason why we make each image the target image and calculate the average distance.
**Note:** The distance between a target image and itself is zero. 
5. We compare the average distances to a threshold.
6. We remove the target image(mislabelled image) when its average distance exceeds the threshold.

![image](https://user-images.githubusercontent.com/59663734/142935906-405ce329-48d7-43ab-8230-341271216ccc.png)

We use the pre-trained weights of Inception Resnet V1 trained on the VGGFace dataset and have an accuracy of 0.9965 on the LFW dataset. We start by restoring the ```.pb``` file and creating a function ```img_removal_by_embed``` to do the following processes:

**1. Collect all folders:**

```
    # ----collect all folders
    dirs = [obj.path for obj in os.scandir(root_dir) if obj.is_dir()]
    if len(dirs) == 0:
        print("No sub-dirs in ", root_dir)
    else:
        #----dataset range
        if dataset_range is not None:
            dirs = dirs[dataset_range[0]:dataset_range[1]]
```

**2. Initialize our model:**

```
        # ----model init
        sess, tf_dict = model_restore_from_pb(pb_path, node_dict, GPU_ratio=GPU_ratio)
        tf_input = tf_dict['input']
        tf_embeddings = tf_dict['embeddings']
```

**3. Set the method to calculate the distance d:**

```
        # ----tf setting for calculating distance
        with tf.Graph().as_default():
            tf_tar = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape[-1])
            tf_ref = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape)
            tf_dis = tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(tf_ref, tf_tar)), axis=1))
            # ----GPU setting
            config = tf.ConfigProto(log_device_placement=True,
                                    allow_soft_placement=True,
                                    )
            config.gpu_options.allow_growth = True
            sess_cal = tf.Session(config=config)
            sess_cal.run(tf.global_variables_initializer())
```

**4. Process each folder and create subfolders to move the mislabelled images:**

```
        #----process each folder
        for dir_path in dirs:
            paths = [file.path for file in os.scandir(dir_path) if file.name.split(".")[-1] in img_format]
            len_path = len(paths)
            if len_path == 0:
                print("No images in ",dir_path)
            else:
                # ----create the sub folder in the output folder
                save_dir = os.path.join(output_dir, dir_path.split("\\")[-1])
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
```

**5. Calculate the embeddings:**

```
                # ----calculate embeddings
                ites = math.ceil(len_path / batch_size)
                embeddings = np.zeros([len_path, tf_embeddings.shape[-1]], dtype=np.float32)
                for idx in range(ites):
                    num_start = idx * batch_size
                    num_end = np.minimum(num_start + batch_size, len_path)
```

**6. Calcuate the average distance using the embeddings:**

```
                # ----calculate avg distance of each image
                feed_dict_2 = {tf_ref: embeddings}
                ave_dis = np.zeros(embeddings.shape[0], dtype=np.float32)
                for idx, embedding in enumerate(embeddings):
                    feed_dict_2[tf_tar] = embedding
                    distance = sess_cal.run(tf_dis, feed_dict=feed_dict_2)
                    ave_dis[idx] = np.sum(distance) / (embeddings.shape[0] - 1)
```

**7. Remove the mislabelled images if average distance greater than threshold(1.25):**

```
                # ----remove or copy images
                for idx,path in enumerate(paths):
                    if ave_dis[idx] > threshold:
                        print("path:{}, ave_distance:{}".format(path,ave_dis[idx]))
                        if type == "copy":
                            save_path = os.path.join(save_dir,path.split("\\")[-1])
                            shutil.copy(path,save_path)
                        elif type == "move":
                            save_path = os.path.join(save_dir,path.split("\\")[-1])
                            shutil.move(path,save_path)
```

We run the file and check the folders. We got ```3981``` folders which had ```20079```wrong images in total. In the folders, we see that our algorithm correctly identified the wrong person in Linda Hamilton's folder, and in Bill Murray's folder, we had more than one mislabelled image. However, we see that the algorithm also removed the images of the correct label. Mainly because the images were blurred or fuzzy, or the subject had sunglasses in them or there were pictures when the person was too young or too old. Nevertheless, data cleaning will now allow our NN to train on a more accurate dataset to make better predictions.

![image](https://user-images.githubusercontent.com/59663734/142937113-3235d10a-9a9b-47fe-b4d8-c5d4c6e776de.png)

### 2.3 Custom Face Mask Dataset
Our end goal is to be able to recognize faces with masks. The CASIA dataset already has half a million pictures of faces and we know that by using the Inception Resnet V1 model we can create a face recognition model. What we want to do now is have the same CASIA dataset with the same folders and same pictures but with the persons wearing a mask. We don't have such as dataset so we need to create one. What we want to do is to show our AI the picture of a person **without** a mask, then a picture of the same person **with** a mask and tell him that it is the same person. 

![image](https://user-images.githubusercontent.com/59663734/142997230-bc4e6fb0-4122-4cdd-8e2f-8a7eb61b3a4b.png)

In order to achieve the process above, we need to have our mask in ```png``` format. PNG formats had 4 channels. The fourth channel is used to describe transparency. I will use the Dlib library which is pre-trained to recognize 68 landmark points that cover the jaw, chin, eyebrows, nose, eyes, and lips of a face. The numbers 48 to 68 are those for the mouth as shown below.

![image](https://user-images.githubusercontent.com/59663734/143016227-3df5cba5-8a75-4c4f-8556-28ebc819e8ad.png)


We start by creating a function ```detect_mouth``` which we will use to read the face landmarks from 48 to 68 and calculate the coordinates:

```
            #----get the mouth part
            for i in range(48, 68):
                x.append(landmark.part(i).x)
                y.append(landmark.part(i).y)

            y_max = np.minimum(max(y) + height // 3, img_rgb.shape[0])
            y_min = np.maximum(min(y) - height // 3, 0)
            x_max = np.minimum(max(x) + width // 3, img_rgb.shape[1])
            x_min = np.maximum(min(x) - width // 3, 0)

            size = ((x_max-x_min),(y_max-y_min))#(width,height)
```


In another function ```mask_wearing``` we first process the folders and create directories for each folder in the main folder. Then we randomly select a PNG mask image from the folder:

```
                        if size is not None: #there is a face
                            # ----random selection of face mask
                            which = random.randint(0, len_mask - 1)
                            item_name = mask_files[which]
```

We read the image with ```cv2.IMREAD_UNCHANGED``` to make sure the image has 4 channels. We resize it based on our mouth detection coordinates found before. We use ```cv2.threshold``` to make the values of the image of the mask ```0```(black) or ```255```(white), i.e, we have the image of a white mask with black background. We use ```cv2.bitwise_and``` to create the mask of the face mask:

```
                            # ----face mask process
                            item_img = cv2.imread(item_name, cv2.IMREAD_UNCHANGED)
                            item_img = cv2.resize(item_img, size)
                            item_img_bgr = item_img[:, :, :3]
                            item_alpha_ch = item_img[:, :, 3]
                            _, item_mask = cv2.threshold(item_alpha_ch, 220, 255, cv2.THRESH_BINARY)
                            img_item = cv2.bitwise_and(item_img_bgr, item_img_bgr, mask=item_mask)
```

We declare the coordinates of our Region of Interest(ROI) from the mouth detection values. We create an invert mask with ```cv2.bitwise_not``` of the face mask and then use ```cv2.bitwise_and``` to mask the face mask onto the person's face:

```
                            # ----mouth part process
                            roi = img[y_min:y_min + size[1], x_min:x_min + size[0]]
                            item_mask_inv = cv2.bitwise_not(item_mask)
                            roi = cv2.bitwise_and(roi, roi, mask=item_mask_inv)
```

We then add the two images: face mask and face:

```
                            # ----addition of mouth and face mask
                            dst = cv2.add(roi, img_item)
                            img[y_min: y_min + size[1], x_min:x_min + size[0]] = dst
```


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143057055-327f0114-8370-493c-8c72-5d55bff2fbab.png" />
</p>

The face masks have successfully been added to the images. Although we have some side face images, we cannot really modify the mask to fit in each image correspondingly so we can say it is a satisfying result. 

## Phase 3: Implementation
We will use the FaceNet concept to implement our Face Recognition with Mask model. In Phase 2, we already did Face Detection to perform Face Alignment whereby we cropped our image with a margin value of ```40```. We will not build an Anti-Spoofing or Face Liveness Detection for now. We will train our model for a first time and then use various Data Augmentation techniques to improve our training accuracy. The process flow of a face recognition model is shown below:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142723211-05e51b72-8794-442e-b1fa-ae9f5a6ed9bc.jpg" />
</p>


### 3.1 FaceNet
FaceNet is a deep neural network used for extracting features from an image of a person’s face. It was proposed  in 2015 by three Google Researchers, Florian Schroff, Dmitry Kalenichenko, and James Philbin, in the paper titled _FaceNet: A Unified Embedding for Face Recognition and Clustering._ It achieved state-of-the-art results in the many benchmark face recognition dataset such as **Labeled Faces in the Wild (LFW)** and Youtube Face Database.

FaceNet learns a mapping from face images to a compact **Euclidean Space** where distances directly correspond to a measure of face similarity. Then it uses the **Triplet Loss function** to train this architecture. FaceNet can achieve state-of-the-art performance (record ```99.63%``` accuracy on ```LFW```, ```95.12%``` on Youtube Faces DB) using only ```128-bytes``` per face.

FaceNet looks for an embedding f(x) from an image into feature space <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbb{R}^{d}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbb{R}^{d}" title="\mathbb{R}^{d}" /></a> (where d is normally 128), such that the squared L2 distance between all face images of the same identity is small, whereas the distance between a pair of face images from different identities is large.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143772229-01d04a66-a215-435f-8d98-b28ce76f464c.png" />
</p>

Whereas previously used losses encourage all faces of the same identity onto a single point in <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbb{R}^{d}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbb{R}^{d}" title="\mathbb{R}^{d}" /></a>, the triplet loss additionally tries to enforce a margin between each pair of faces from one person (anchor and positive) to all others’ faces. This margin enforces discriminability to other identities. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143772288-cb9ee80e-44dc-43b1-b817-73027c82cbe4.png" />
</p>

### 3.2 Resnet Network
FaceNet uses ```Zeiler & Fergus``` architecture and ```GoogLeNet``` style ```Inception``` model as its underlying architecture. Since we will be using the ```Inception ResNet V1``` Network, we will start by first understanding what is a ResNet Network.

Resnet published in 2016 in the paper titled: _Deep Residual Learning for Image Recognition_ by Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun showed a solution to the paradox of the increase in training and testing error when increasing layers in a CNN. As shown in the graph below, a 56-layer CNN gives more error rate on both training and testing dataset than a 20-layer CNN architecture. This happens due to the phenomenon of the **Vanishing gradient** during backpropagation whereby the gradient becomes 0.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143995794-fb0b3f6a-4fff-4ce2-bd37-ddfa818e3a67.png" />
</p>

In order to solve the vanishing gradient problem(due to the use of L1 and l2 regularizer), the architecture introduced the **skip connections** which skips training from a few layers and connects directly to the output. This will avoid that problem as gradient can backpropagate via the skip connection. Even if the main path is zero, performance will not degrade as information will flow through skip connection during forward propagation.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143997344-e25136d5-e07d-4b24-b4cb-ae70ce314d84.png" />
</p>

The below graphs compare the accuracies of a **plain network** with that of a **residual network**. Note that with increasing layers a 34-layer plain network’s accuracy starts to saturate earlier than ResNet’s accuracy.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143997594-971407c0-bd44-4aa5-a021-53996267de86.png" />
</p>

I propose this simple ResNet archietecture of four ResNet blocks and four max pooling. We will flatten our layer and feed it into a FC of ```128``` units to represent our embedding. 


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/142753156-d5bb6d19-ab56-42f2-9522-d06ac374dd66.png" />
 </p>
<p align="center">
  Fig. The Resnet architecture with the Resnet Block.
  </p>
  
We start by building our Resnet Block which will be duplicated ```4``` times in the whole architecture. In our function ```resnet_block```, we define a kernel size of  ```3 x 3```, ```32``` filters, with padding = ```"same"```, a ```l2``` regularizer and a ```relu``` activation function.
  
  
```
    #----models
    def resnet_block(self,input_x, k_size=3,filters=32):
        net = tf.layers.conv2d(
            inputs=input_x,
            filters = filters,
            kernel_size=[k_size,k_size],
            kernel_regularizer=tf.keras.regularizers.l2(0.1),
            padding="same",
            activation=tf.nn.relu
        )
        net = tf.layers.conv2d(
            inputs=net,
            filters=filters,
            kernel_size=[k_size, k_size],
            kernel_regularizer=tf.keras.regularizers.l2(0.1),
            padding="same",
            activation=tf.nn.relu
        )

        net_1 = tf.layers.conv2d(
            inputs=input_x,
            filters=filters,
            kernel_size=[k_size, k_size],
            kernel_regularizer=tf.keras.regularizers.l2(0.1),
            padding="same",
            activation=tf.nn.relu
        )

        add = tf.add(net,net_1)

        add_result = tf.nn.relu(add)

        return add_result
```

Next, we define a function ```simple_resnet``` where we will design the whole architecture. We coede the first Resnet block and the max pooling layer:

```
        net = self.resnet_block(tf_input,k_size=3,filters=16)
        net = tf.layers.max_pooling2d(inputs=net, pool_size=[2,2], strides=2)
        print("pool_1 shape:",net.shape)
```

We duplicate the above code and increase the number of filters as we go deeper:

```
        net = self.resnet_block(tf_input,k_size=3,filters=16)
        net = tf.layers.max_pooling2d(inputs=net, pool_size=[2,2], strides=2)
        print("pool_1 shape:",net.shape)

        net = self.resnet_block(net, k_size=3, filters=32)
        net = tf.layers.max_pooling2d(inputs=net, pool_size=[2, 2], strides=2)
        print("pool_2 shape:", net.shape)

        net = self.resnet_block(net, k_size=3, filters=48)
        net = tf.layers.max_pooling2d(inputs=net, pool_size=[2, 2], strides=2)
        print("pool_3 shape:", net.shape)

        net = self.resnet_block(net, k_size=3, filters=64)
        net = tf.layers.max_pooling2d(inputs=net, pool_size=[2, 2], strides=2)
        print("pool_4 shape:", net.shape)
```

We then flatten our layer:

```
        #----flatten
        net = tf.layers.flatten(net)
        print("flatten shape:",net.shape)
```

We feed into into a fully connected layer with dropout and units = ```128``` which represent the ```encoding```.

```
        #----dropout
        net = tf.nn.dropout(net,keep_prob=tf_keep_prob)

        #----FC
        net = tf.layers.dense(inputs=net,units=128,activation=tf.nn.relu)
        print("FC shape:",net.shape)

        #----output
        output = tf.layers.dense(inputs=net,units=class_num,activation=None)
        print("output shape:",output.shape)
```

### 3.3 Inception Network
When designing a layer for a convNet, we need to pick the type of filters we want: ```1x1```, ```3x3``` or ```5x5``` or even the type of pooling. To get rid of this conundrum, the inception layer allows us to implement them all. So why do we use filters of different sizes? For our example, our image will be of the same dimension but the **target** in the image may be of different sizes, i.e, a person may stand far from the camera or one may be close to it. Having different kernel size allow us to extract features of different size. 

We can start by understanding the Naive version of the Inception model where we apply different types of kernel on an input and concatenate the output as shown below. The idea is instead of us selecting the filter sizes, we use them all and concatenate their output and let the NN learn whichever combination of filter sizes it wants. However, the problem with this method is the **computational cost**. 

Deep Convolutional Networks are computationally expensive. Also, very deep networks are susceptible to overfitting -  it is hard to pass gradient updates through the entire network.

![image](https://user-images.githubusercontent.com/59663734/142761227-875b8713-1edb-4058-a6c6-7f396d8cce1e.png)

#### 3.3.1 Network in Network

If we look at the computational cost of the ```5x5``` filters of the ```28x28x192``` input volume, we have a whopping ```120M``` multiplies to perform. It is important to remember that this is only for the ```5x5``` filter and we still need to compute for the other 2 filters and pooling layer. A solution to this is to implement a ```1x1``` convolution before the ```5x5``` filter that will output the same ```28x28x32``` volume but will reduce the number of multiplies by one-tenth.

![image](https://user-images.githubusercontent.com/59663734/142761522-9a60199a-2044-4e26-b975-aff7e6da3a81.png)

How does this work?
A ```1x1``` convolution also called a ```Network in network``` will take the element-wise product between the 192 numbers(example above) in the input and the 192 numbers in the filter and apply a relu activation function and output a single number. We will have a number of filters so the output will be ```HxWx#filters```.

If we want to reduce the height and width of an input then we can use pooling to do so, however, if we want to reduce the number of channels of an input(192) then we use a ```1x1x#channels``` filter with the numbers of filters equal to the number of channels we want to output. In the example above in the middle section, we want the channel to be 16 so we use 16 filters. 

We create a bottleneck by shrinking the number of channels from 192 to 16 and then increasing it again to 32. This allows us to diminish dramatically the computational cost which is now about ```12.4 M ``` multiplies.  The ```1x1``` convolution is an important building block in the inception network which allows us to go deeper into the network by maintaining the computational cost and learning more features.


#### 3.3.2 Inception with Dimension Reduction
To reduce our computational cost we should modify our architecture and add 1x1 convolution to it. As shown above, the 1x1 filters will allow us to have fewer weights therefore fewer calculations and therefore faster inference. The figure below shows one Inception module. The Inception network just puts a lot of these modules together.

![image](https://user-images.githubusercontent.com/59663734/142762642-b684146a-28c7-4c16-b7ea-26d6a67d8b18.png)

We have ```9``` of the inception block concatenate to each other with some additional max pooling to change the dimension. We should note that the last layer is a fully-connected layer followed by a softmax layer to make predictions but we also have two side branches coming from the hidden layers trying to make predictions with a softmax output. This helps ensure that the features computed in the hidden layers are also good to make accurate predictions and this helps the network from overfitting. 

![image](https://user-images.githubusercontent.com/59663734/142762952-90a602b5-5fb7-43c7-8589-e41c02f22647.png)

### 3.4 Inception-Resnet V1 Network
Inspired by the performance of the ResNet, a hybrid inception module was proposed. There are two sub-versions of Inception ResNet, namely **v1** and **v2**. Inception-ResNet v1 has a computational cost that is similar to that of Inception v3 and Inception-ResNet v2 has a computational cost that is similar to that of Inception v4.

Below are some features of the Inception ResNet architecture:

- For residual addition to work, the input and output after convolution must have the same dimensions. Hence, we use 1x1 convolutions after the original convolutions, to match the depth sizes (Depth is increased after convolution).
- The pooling operation inside the main inception modules were replaced in favor of the residual connections.
- Networks with residual units deeper in the architecture caused the network to “die” if the number of filters exceeded 1000. Hence, to increase stability, the authors scaled the residual activations by a value around 0.1 to 0.3.

It was found that Inception-ResNet models were able to achieve higher accuracies at a lower epoch. We will use this network to train and test our Face Recognition with Masks model.

![image](https://user-images.githubusercontent.com/59663734/142763781-1a990187-307c-45db-9f61-01bf89b1c861.png)

We will use the TensorFlow implementation of the Inception ResNet V1 architecture proposed by David Sandberg. He proposed two models, one trained on the CASIA-Webface dataset and the other on the VGGFace2 dataset. They achieved an accuracy of ```99.05%``` and ```99.65%``` respectively. We will **not** use the pre-trained model as we will train our model from scratch but we will definitely use the metrics as a benchmark for our model.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143538914-da809328-f8ca-4393-b465-df1251fa6e06.png" />
</p>




 ### 3.5 First Training(Evaluation: No Mask Dataset)
 We now train our model on the CASIA dataset with ```No Masks``` and the custom CASIA Dataset we made with ```Masks```. We will evaluate the performance of our model on the ```LFW``` dataset which contains images with ```No Masks```. The hyperparameters which we will need to tune are as follows:
 
 - model_shape :  [None, 112, 112, 3] or [None, 160, 160, 3]
 - infer_method :  inception_resnet_v1 or inception_resnet_v1_reduction
 - loss_method :  cross_entropy or arcface
 - opti_method :  adam
 - learning_rate :  0.0001 or 0.0005
 - embed_length :  128 or 256
 - epochs :  40 or above
 - GPU_ratio :  [0.1, 1]
 - batch_size :  32 or 48 or 96 or 128
 - ratio :  [0.1, 1.0]
 
 
I tested it with only ```0.2%``` of the dataset for testing purposes and we got low values for the training and testing accuracy and some weird-looking graphs as expected. I increased the ratio(ratio of images of the whole dataset) to ```0.01``` but reduced the batch to ```32``` size as my GPU would run out of memory and the results started to be promising with the test accuracy at nearly ```72.9%```. However, we see our training accuracy at ```100%``` which would be ideal but I suspect ```overfitting``` of data. In order to avoid this, we need to feed the model more data so I increased the ratio to ```0.1```. The training accuracy increased slightly but the testing accuracy increased by nearly ```20%```. We see that the testing accuracy never exceeded the training accuracy. With only a testing accuracy of ```86.93%``` the model would work but it will not be a reliable one. We need to have an accuracy nearing ```98%``` or ```99%``` in order to be used in an industry setting. However, my GPU(RTX 3060-6GB memory) ran out of memory so I had to stop the training for the time being till I find another way of training the model.
 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143400671-b8a25fe3-366a-4016-96fc-d7d07d198162.png" />
</P>

Below is the schema for the training and testing process on the different datasets we have:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143473743-3fb9b740-8380-420c-8127-43b6fd82857f.png" />
</p>

 ### 3.6 Data Augmentation
With a first initial training, the accuracy of the model was moderate. One possible way to increase the accuracy would be to have more data. But how much? Instead of finding new images, I would "create" these images using Data Augmentation techniques. I would use five data augmentation techniques namely: 
 
 1. Random Crop
 2. Random Noise
 3. Random Rotation
 4. Random Horizontal Flip
 5. Random Brifhtness Augmentation

Instead of using Tensorflow's Data Augmentation API, I would create the scripts and generate the images using OpenCV packages and numpy. 
 
 <p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143091509-8ba772f6-3cb1-46a7-806c-cb786976af14.png" />
</p>


**1. Random Crop**

We want to create a script to crop randomly our images to become ```150x150```. We create a frame of this size and in a small 10x10 square on the top left, we generate random points and use this as our first x-y values of the frame. We position the frame and then we crop the image:

```
                # ----random crop
                if random_crop is True:
                    # ----resize the image 1.15 times
                    img = cv2.resize(img, None, fx=1.15, fy=1.15)

                    # ----Find a random point
                    y_range = img.shape[0] - img_shape[0]
                    x_range = img.shape[1] - img_shape[1]
                    x_start = np.random.randint(x_range)
                    y_start = np.random.randint(y_range)

                    # ----From the random point, crop the image
                    img = img[y_start:y_start + img_shape[0], x_start:x_start + img_shape[1], :]
```
 
 **2. Random Noise**
 
For the random noise, we create a mask which is a NumPy array of the same size of the image with only one channel. We then create a uniformly-distributed array of random numbers. If the pixel value is greater than a threshold(```240```) then it is set to ```255``` else it becomes ```0```. If the mask pixel value is ```255```, we use ```cv2.bitwise_and()``` operation else we pass.
 
 ```
                 # ----random noise
                if random_noise is True:
                    uniform_noise = np.empty((img.shape[0], img.shape[1]), dtype=np.uint8)
                    cv2.randu(uniform_noise, 0, 255)
                    ret, impulse_noise = cv2.threshold(uniform_noise, 240, 255, cv2.THRESH_BINARY_INV)
                    img = cv2.bitwise_and(img, img, mask=impulse_noise)
 ```
 
**3. Random Rotation**

We set our angle range from ```-60 to 60``` degrees. We define our center point of rotation and use ```cv2.warpAffine``` to get the reuslt:

```
               # ----random angle
                if random_angle is True:
                    angle = np.random.randint(-60, 60)
                    height, width = img.shape[:2]
                    M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
                    img = cv2.warpAffine(img, M, (width, height))
```

**4. Random Horizontal Flip**

We don't want to flip our image vertically as we do not expect to see someone upside down when doing inference. So we use only ```Flip_type = 1``` for the horizontal flip. 

```
                # ----random flip
                if random_flip is True:
                    flip_type = np.random.choice(flip_list)
                    if flip_type == 1:
                        img = cv2.flip(img, flip_type)
```


**5. Random Brightness Augmentation**

 We calculate the mean brightness and set a 30% variation range: ```0.3xnp.mean(img)```. We find a number in the range as the new brightness and normalize the image by dividing by the average value. We use ```np.clip()``` to apply the brightness:

```
                # ----random brightness
                if random_brightness is True:
                    mean_br = np.mean(img)
                    br_factor = np.random.randint(mean_br * 0.7, mean_br * 1.3)
                    img = np.clip(img / mean_br * br_factor, 0, 255)
                    img = img.astype(np.uint8)****
```
 
 
Since our data has now been doubled we divide the batch size by 2 in order to have the same number of data in one batch as before. We also reverse the paths of the sub-folders in the directories of the CASIA mask and without mask such that in half a batch we have the original images and in the other half we have the data augmented images. We then re-train the model.
 
 
### 3.7 Second Training with Data Augmentation
#### 3.7.1 Evaluation: No Mask Dataset
After performing data augmentation on our pictures, we train the model and fine tune the hyperparameters as before. We are still using the ``LFW``` as our validation set when training the model. Below are the parameters to be tuned: 

- model_shape :  [None, 112, 112, 3] or [None, 160, 160, 3]
- infer_method :  inception_resnet_v1
- loss_method :  cross_entropy or arcface
- opti_method :  adam
- learning_rate :  0.0002 or 0.0005
- embed_length :  128 or 256
- epochs :  40 or 60 or 100 
- GPU_ratio :  None
- batch_size :  32 or 96 or 196
- ratio :  0.1 or 0.4
- process_dict :  {'rdm_flip': True, 'rdm_br': True, 'rdm_crop': True, 'rdm_angle': True, 'rdm_noise': True}

I set the ratio to ```0.4``` and the batch size to ```196```, and the accuracy increased from ```86.93%``` from our last training to a whopping ```92.07%``` - an increase of nearly ```6%```. Using the same settings, I only decreased the learning rate to ```0.0002``` and the testing accuracy increased slightly to ```0.9618```. 

![image](https://user-images.githubusercontent.com/59663734/143456873-2170f8de-1b22-4d98-a063-2ed1d923966b.png)
![image](https://user-images.githubusercontent.com/59663734/143496027-d14a7b6b-8549-4b5a-b7ef-4efe4088169a.png)

We clearly see a great improvement in our testing accuracy but we need to do more tests to ensure the robustness of the model.

#### 3.7.2 Evaluation: Mask Dataset
What we have been doing till now is train our images on the ```CASIA``` dataset with masks and without masks and then test it onto our **without** mask ```LFW``` dataset. The accuracy we got before was for face recognition **without** masks. We need to propose another method for the evaluation of faces **with** masks. Out steps are as follows:

1. Use a new dataset that has never been used in our FaceNet training.
2. Select 1000 different class images(1000 persons) - they are regarded as our face database(reference data: ref_data): No Mask Folder
3. In these 1000 class images make them wear masks - these images will be used as test images(target data: tar_data): Mask Folder
4. We calculate the embeddings of both images(masks and without masks) and use them to do face matching.
 
For the example, below we assume an image as a 3-dimensional embedding. We calculate the euclidean distance using the ```d``` function explained before for the target image(image with masks) and the images in our No Mask folder. If the indexes of both images match and the distance is below a threshold(0.3) then we conclude we have a correct matching.
 
<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143234725-6b87b1dd-151a-48ff-a178-f1abaa6f10e3.png" />
</p>

 We start by creating an ```evaluation``` function which will:
 
**1. Get our test images(images with masks):**

```
    #----get test images
    for dir_name, subdir_names, filenames in os.walk(test_dir):
        if len(filenames):
            for file in filenames:
                if file[-3:] in img_format:
                    paths_test.append(os.path.join(dir_name,file))

    if len(paths_test) == 0:
        print("No images in ",test_dir)
        raise ValueError
```
 
**2. Get our face images(images without masks):**

```
    #----get images of face_databse_dir
    paths_ref = [file.path for file in os.scandir(face_databse_dir) if file.name[-3:] in img_format]
    len_path_ref = len(paths_ref)
    if len_path_ref == 0:
        print("No images in ", face_databse_dir)
        raise ValueError
```
 
 **3. Initialize our model by restoring the pb file to get the embeddings:**

```
    #----model init
    sess, tf_dict = model_restore_from_pb(pb_path, node_dict, GPU_ratio=GPU_ratio)
    tf_embeddings = tf_dict['embeddings']
```

**4. Create the formula to calculate the euclidean distance:**

```
    #----tf setting for calculating distance
    with tf.Graph().as_default():
        tf_tar = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape[-1]) #shape = [128]
        tf_ref = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape) #shape = [N,128]
        tf_dis = tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(tf_ref, tf_tar)), axis=1))
```
 
**5. Get embeddings:**

```
    #----get embeddings
    embed_ref = get_embeddings(sess, paths_ref, tf_dict, batch_size=batch_size) #use get_embeddings fucntion
    embed_tar = get_embeddings(sess, paths_test, tf_dict, batch_size=batch_size)
    print("embed_ref shape: ", embed_ref.shape)
    print("embed_tar shape: ", embed_tar.shape)
```

**6. Calculate the distance and check if it is less than the threshold(0.8):**

```
    #----calculate distance and get the minimum index
    feed_dict_2 = {tf_ref: embed_ref}
    for idx, embedding in enumerate(embed_tar): #we do face matching one by one
        feed_dict_2[tf_tar] = embedding
        distance = sess_cal.run(tf_dis, feed_dict=feed_dict_2)
        arg_temp = np.argsort(distance)[0] #get index of minimum value
        arg_dis.append(arg_temp)
        dis_list.append(distance[arg_temp])
```

**7. We then check if we have the correct predictions. We do a first check with the threshold and a second check with the indexes.**

```
    for idx, path in enumerate(paths_test):
        answer = path.split("\\")[-1].split("_")[0] #index of target image

        arg = arg_dis[idx]
        prediction = paths_ref[arg].split("\\")[-1].split("_")[0] #index of reference image

        dis = dis_list[idx]

        if dis < threshold: #check for threshold
            if prediction == answer: #check if both index are same
                count_o += 1
            else:
                print("\nIncorrect:",path)
                print("prediction:{}, answer:{}".format(prediction,answer))
        else:
            count_unknown += 1
            print("\nunknown:", path)
            print("prediction:{}, answer:{}, distance:{}".format(prediction,answer,dis))

```

We use the evaluation function and test:

1. The pre-trained Inception ResNet V1 model trained on CASIA-Webface dataset
2. The pre-trained Inception ResNet V1 model trained on VGGFace2 dataset
3. Our model **before** Data Augmentation
4. Our model **after** Data Augmentation

Below are the test results:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143469476-ec8e6064-3b18-4f53-b074-1ec8fd6578eb.png" />
</p>

When evaluating the pre-trained weights of the model ```20180408-102900``` on our mask dataset, we got only an accuracy of ```16.3%``` at a threshold of ```0.7``` and nearly thrice that at a threshold of ```0.8```. The same is seen for the model ```20180402-114759``` with slightly better accuracy. This clearly shows that we would not have used the model for face recognition with masks. Our model before data augmentation has a shockingly low accuracy on both thresholds. However, since we reached only an accuracy of ```0.8693``` of the LFW dataset then we can conclude the model was not that robust. After data augmentation, our model accuracy increased sharply on both the LFW dataset and the masks dataset with a maximum accuracy of ```99.98%``` at a threshold of 0.8. Our model surpassed the accuracy of the pre-trained weights of the original Inception ResNet V1 model and has been optimized to perform better at recognizing faces with masks.

After performing data augmentation and evaluating our model on both the LFW dataset and the masks dataset, we update our schema:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143473665-ac07f435-7d89-4443-b43c-d9ad05425af5.png" />
</p>

While the accuracy values may seem promising, I suspect we may still be overfitting the data and this is due to the **unbalanced** CASIA dataset which we have. I propose we do a more fair **sampling** of our data for training as explained below. 

 ### 3.8 Third Training(Evaluation: Mask Dataset with Stratified Sampling)
 In the previous training, we introduced a ```sampling bias```. For example, if our first class in our CASIA dataset has 100 images and the second class has 10 images then when using a ratio of 0.4, we are taking 40 from the first folder and only 4 from the second folder. This disparity of the number of images in the folders creates this sampling bias. A better approach would be to ensure the test set is representative of the various classes in the whole dataset. So we introduce ```stratified sampling``` whereby the classes are divided into homogeneous subgroups called ```strata``` and the correct number of images is sampled from each stratum to guarantee the test set is representative of the whole dataset.

We begin by exploring how many classes have less than ```10``` images and how much have greater than ```100``` images. We got ```195``` for the first condition and ```859``` for the second condition. While it is difficult to remove classes with less than 10 images, we cannot remove both sets of classes as we will lose about 1000 classes. What we can do is randomly select a constant x(2 or 5 or 15) number of images from all the different classes. By doing so we reduce the number of images we are training on but we also gain in the time to train the model. To increase our data(since we are selecting only (2 or 5 or 15) images from all the classes), we perform more data augmentation. For each image, we have selected we create a copy of ```4``` images on which we do data augmentation. For example, if from a folder of 10 images we selected only 5 images then we see that we have reduced by 50% the number of images on which the AI will train. However, we will now perform data augmentation on each of the 5 images such that the 5 images will multiply by 4 to become 20 images. The images will be as followed:

1. Original image without mask
2. Original image without mask with Data augmentation
3. Original image with random mask with Data Augmentation
4. Original image with random mask with Data Augmentation

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143391065-01892c94-7cb6-498c-b703-8f2420b58754.png" />
</p>


We change our ```get_4D_data``` function to accommodate for the changes described above. We create a variable ```aug_times``` and assign it the value ```4``` since each image will be augmented to 4 pictures. We have a dictionary ```p_dict_1``` where we input the type of data augmentation we will do. We enumerate in the variable to apply those data augmentation.

```
aug_times = 4
path = [np.random.choice(paths)]

img_shape = [112,112,3]
batch_data_shape = [aug_times]
batch_data_shape.extend(img_shape)
batch_data = np.zeros(batch_data_shape,dtype=np.float32)

p_dict_1 = {'rdm_mask':False,'rdm_crop':True,'rdm_br':True,'rdm_blur':True,'rdm_flip':True,'rdm_noise':False,'rdm_angle':True}
p_dict_2 = {'rdm_mask':True,'rdm_crop':True,'rdm_br':True,'rdm_blur':True,'rdm_flip':True,'rdm_noise':False,'rdm_angle':True}
p_dict_3 = {'rdm_mask':True,'rdm_crop':True,'rdm_br':True,'rdm_blur':True,'rdm_flip':True,'rdm_noise':False,'rdm_angle':True}

for i in range(aug_times):
    if i == 0:
        temp = get_4D_data(path,img_shape,process_dict=None)
        
    elif i == 1:
        temp = get_4D_data(path,img_shape,process_dict=p_dict_1)
    elif i == 2:
        temp = get_4D_data(path,img_shape,process_dict=p_dict_2)
    elif i == 3:
        temp = get_4D_data(path,img_shape,process_dict=p_dict_3)
    batch_data[i] = temp[0]
```
<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143499077-b0a8a568-0e9e-404e-906f-3439a80284b5.png" />
</p>


We then create another variable ```select_num``` where we will input the number of images we want to select from each class. We check if it is an integer and greater than 1. If so, we reset our training paths and labels. ```paths``` is a list because we use ```append``` to collect images from each folder. We shuffle that list and using ```np.min()``` we select the minimum between ```select_num``` or ```len(paths)```,i.e, we take all pictures in the latter condition. We transform the list to a NumPy array and shuffle.

```
                    if select_num >= 1:
                        #----reset paths and lables
                        train_paths_ori = list()
                        train_labels_ori = list()
                        #----select images from each folder
                        for paths,labels in zip(self.train_paths,self.train_labels):
                            np.random.shuffle(paths)
                            num = np.minimum(len(paths), select_num)
                            train_paths_ori.extend(paths[:num])
                            train_labels_ori.extend(labels[:num])
                        #----list to np array
                        train_paths_ori = np.array(train_paths_ori)
                        train_labels_ori = np.array(train_labels_ori)
                        #----shuffle
                        indice = np.random.permutation(train_paths_ori.shape[0])
                        train_paths_ori = train_paths_ori[indice]
                        train_labels_ori = train_labels_ori[indice]

```

We begin to train the model with a high epoch number of ```100```. We reduce our batch size to ```96``` to avoid our GPU to run out of memory. We have a ```select_num = 2``` for faster training and we keep all the other parameters unchanged. After ```33 hours``` of training, we managed to get a decent accuracy of ```0.9693```. Now we can be sure we are not overfitting as much when solving the bias sampling issue.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143495406-beda56e4-0c7d-46a6-8cb7-b65e312a12a2.png",
  <img src= "https://user-images.githubusercontent.com/59663734/143495421-019f0c5c-c6f4-492e-a708-44a9a54c24d0.png" />
</p>
<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143495785-7ed4435c-27f7-4262-9bf3-2eff20e578de.png" />
</p>

Below are the test results for our whole training process till the beginning. We observe that the difference when selecting ```2``` or ```5``` images from each class and ```15``` images from each class is very little(```0.9947``` compared to ```0.9941```). However, the average time of one epoch was ```65``` min with a GPU of RTX 2080 Ti. We see that when we selected only 2 images from each folder and perform data augmentation then our accuracy was nearly the same and our average time for one epoch was only around ```10``` min. Since now we solved the data imbalance problem, even when our selected number is small we can still reach a high accuracy. 

![image](https://user-images.githubusercontent.com/59663734/143497574-364ba31f-784a-419a-a7ee-3480a60fb0f5.png)

We update for the final time our schema which resumes our whole training and testing accuracies:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143497506-cda11a9f-bfa2-410d-9d1f-a2faa6f6295e.png" />
</p>

Now after being confident that we got a robust model, it is time for ```real-time face recognition with masks```.
 
 ### 3.9 Real-time Face Recognition
We now come to the time for the real test - real-time face recognition. Our objective is to recognize a person who is wearing a mask. We start by reading the image from a camera input. We need to process the image from BGR to RGB. Using our pre-trained face mask SSD model we had, we perform the face detection and crop the face. We send this image to our face recognition model for face matching. If a face is detected, our face mask detection model will draw a rectangle showing if the person is wearing a mask or not. We use the face coordinates from the face detection model to crop the image and our face recognition model will perform the embedding and assign name to the image with the least distance. A schema of the process is shown below:
 
 
<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143441698-3032a8ce-a397-4488-9788-332ce6b106b9.png" />
</p>

For the real-time recognition, the process is divided into three phases:

1. Real Time streaming
2. Add Face Mask Detection
3. Add Face Recognition

#### 3.9.1 Real Time Streaming

In a function called ```stream``` we have a while loop which will stream video directly from our webcam:

```
def stream(camera_source=0,resolution="480",to_write=False,save_dir=None):
    
    #----Video streaming initialization
    cap,height,width,writer = video_init(camera_source=camera_source, resolution=resolution, to_write=to_write, save_dir=save_dir)

    #----Get an image
    while(cap.isOpened()):
        ret, img = cap.read()#img is the original image with BGR format. It's used to be shown by opencv

        if ret is True:
            #----image display
            cv2.imshow("demo by Yudhisteer", img)

            #----image writing
            if writer is not None:
                writer.write(img)

            #----keys handle
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        else:
            print("get images failed")
            break

    #----release
    cap.release()
    cv2.destroyAllWindows()
    if writer is not None:
        writer.release()
```

We test it:

https://user-images.githubusercontent.com/59663734/143538699-a92a0b30-1742-49e5-9e27-a7103585d399.mp4

#### 3.9.2 Add Face Mask Detection
We upload our face mask model from our pb file and create two variables: ```margin``` and ```i2dclass```:
```
    face_mask_model_path = r'face_mask_detection.pb'
    margin = 40
    id2class = {0: 'Mask', 1: 'NoMask'}
```

We initialize our face detection model:

```
    # ----face detection init
    fmd = FaceMaskDetection(face_mask_model_path, margin, GPU_ratio=None)
```

We now need to convert our image from BGR to RGB and do normalization. We resize our image and increase the dimension by 1:

```
            # ----face detection
            img_fd = cv2.resize(img_rgb, fmd.img_size)
            img_fd = np.expand_dims(img_fd, axis=0)
```

We perform the inference and check if we detect a mask. We draw a green rectangle if we detect one and if not a red rectangle. We display the information just above the rectangle:

```
            # ----draw rectangle
            bboxes, re_confidence, re_classes, re_mask_id = fmd.inference(img_fd, height, width)
            if len(bboxes) > 0:
                for num, bbox in enumerate(bboxes):
                    class_id = re_mask_id[num]
                    if class_id == 0:
                        color = (0, 255, 0)  # (B,G,R) --> Green(with masks)
                    else:
                        color = (0, 0, 255)  # (B,G,R) --> Red(without masks)
                    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)
                    cv2.putText(img, "%s: %.2f" % (id2class[class_id], re_confidence[num]), (bbox[0] + 2, bbox[1] - 2),
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
```

We test it:

https://user-images.githubusercontent.com/59663734/143541830-d27a53d7-f267-4108-ae35-811f97ee663e.mp4


#### 3.9.3 Add Face Recognition
For the third phase, we have the Microsoft Celebrity dataset to test our model which contains ```85,742``` persons' faces. I will insert my image in the database and check if the model can recognize me among all these people.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143551710-01c61845-6534-4d6d-a04b-35f45b638d34.png" />
</p>


We restore our face recognition model from our ```pb_model_select_num=15.pb``` file and initialize our face recognition model:

```
    # ----face recognition init
    sess, tf_dict = model_restore_from_pb(pb_path, node_dict, GPU_ratio=None)
    tf_input = tf_dict['input']
    tf_embeddings = tf_dict['embeddings']
```

We now read the images from the database: We then a batch data of ```32``` to read our images, normalize the data and get the embeddings:

```
    #----read images from the database
    d_t = time.time()
    paths = [file.path for file in os.scandir(ref_dir) if file.name[-3:] in img_format]
    len_ref_path = len(paths)
    if len_ref_path == 0:
        print("No images in ", ref_dir)
    else:
        ites = math.ceil(len_ref_path / batch_size)
        embeddings_ref = np.zeros([len_ref_path, tf_embeddings.shape[-1]], dtype=np.float32)
```

Using a batch data of ```32``` to read our images, we normalize the data and get the embeddings:
```
        for i in range(ites):
            num_start = i * batch_size
            num_end = np.minimum(num_start + batch_size, len_ref_path)

            batch_data_dim =[num_end - num_start]
            batch_data_dim.extend(model_shape[1:])
            batch_data = np.zeros(batch_data_dim,dtype=np.float32)

            for idx,path in enumerate(paths[num_start:num_end]):
                # img = cv2.imread(path)
                img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
                if img is None:
                    print("read failed:",path)
                else:
                    #print("model_shape:",model_shape[1:3])
                    img = cv2.resize(img,(model_shape[2],model_shape[1]))
                    img = img[:,:,::-1]#change the color format
                    batch_data[idx] = img
            batch_data /= 255
            feed_dict[tf_input] = batch_data
            embeddings_ref[num_start:num_end] = sess.run(tf_embeddings,feed_dict=feed_dict)
```

We set our euclidean distance equation to calculate the distance:

```
            tf_dis = tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(tf_ref, tf_tar)), axis=1))
```

After the face detection step, if a face is detected we get the face coordinates to crop the image, resize and change the dimension to ```4```:

```
                    if len_ref_path > 0:
                        img_fr = img_rgb[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2], :]  # crop
                        img_fr = cv2.resize(img_fr, (model_shape[2], model_shape[1]))  # resize
                        img_fr = np.expand_dims(img_fr, axis=0)  # make 4 dimensions
```

We get the embeddings and calculate the distance and get the **index** of the image of the smaller distance:

```
                        embeddings_tar = sess.run(tf_embeddings, feed_dict=feed_dict) #embeddings of target
                        feed_dict_2[tf_tar] = embeddings_tar[0]
                        distance = sess_cal.run(tf_dis, feed_dict=feed_dict_2)
                        arg = np.argmin(distance)  # index of the smallest distance
```

If the distance of this particular index is also smaller than our threshold(```0.8```), we conclude we have a **match**. We get the name of our image file which is initially an empty variable and display it on top of our rectangle:

```
                        if distance[arg] < threshold: #we have a match
                            name = paths[arg].split("\\")[-1].split(".")[0]

                    cv2.putText(img, "{},{}".format(id2class[class_id], name), (bbox[0] + 2, bbox[1] - 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
```

We execute the program and it took ```307.093s(about 5 min)``` to get the embeddings of ```85743``` people.

https://user-images.githubusercontent.com/59663734/143551087-1b99ce2c-f2f3-44a4-ace9-19206e20c27c.mp4



The test was successful!

## Phase 4: Further Improvement
### 4.1 Face Mask Recognition with Glasses
The model was successful at recognizing people with masks however after several tests we see that there are still some shortcomings of the model whereby if in the target image the person had glasses then the model fails to recognize the person in real-time without glasses and vice versa. One possible solution would be to increase the threshold from ```0.7``` to ```1.0``` but that can also allow incorrect predictions by the model.

One better solution will be similar to what we did when training our model to recognize faces with masks: **recognize faces with glasses**. But where will we get a database with people with glasses? Just as we fabricated our own dataset with masks we will need to create our own dataset with glasses. Using PNG images of glasses, we use our face detection model to detect the eyes of the person and using masking of images we add the glasses to the target image. Our goal is still to recognize people with face masks therefore, similar to what we did in phase three of training whereby 1 picture is replicated to 4 times with data augmentation, our script will now include to randomly choose a glass and a mask as shown below such that for each picture we now create  ```6``` pictures:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143584263-46d97471-a69f-4e4b-b668-e77fb59bf6a6.png" />
</p>

### 4.2 Limits of the System
One shortcoming of the system is recognizing faces from a side view perspective. As shown in the video below, the system fails to provide a prediction for the person when there is no frontal view of the face. The model still works when turning the head from an angle of -60 degrees to 60 degrees but a full 90 degrees head turn will produce no result.

https://user-images.githubusercontent.com/59663734/144132768-a7704e8a-5ba6-41f3-80b5-1ba011f25375.mp4

One possible solution would be to implement the ```One to Many``` face processing technique whereby we generate multiple images with different poses from a single image. Due to this, the network can learn **pose-invariant** representations. We could add it into our data augmentation phase along with the random mask technique.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/144133862-358e4b20-e1db-4580-805f-21a67e38cb89.png" />
</p>


### 4.3 Face Mask Recognition with Sunglasses
No model exists on the market able to recognize someone with sunglasses **and** mask. My next step will be to perform more data augmentation on my image to include sunglasses and masks to train the model to perform ```face mask sunglasses recognition```:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/143573017-ec72abf9-09c0-4231-ad35-7097a70875c7.png" />
</p>

If the model will be able to detect faces with mask and sunglasses then it can also be used as a **surveillance system**. It needs only one image of a person to be able to recognize that individual and if we could get the picture of each person entering the building then in the future we could predict if any of them is the culprit.

## Conclusion
The model was successful at recognizing people with masks. With an accuracy of ```99.84%``` after performing data augmentation and stratified sampling, the model is ready to be deployed in the office. As discussed above, we observe some limits of the model. Training the model on images with and without glasses will be a way to improve the accuracy of our prediction. 

We started with a simple face detection algorithm and use SSD to make a face mask detection model. From there, using the Inception ResNet V1 architecture, we trained our model from scratch and tested the accuracy. Due to overfitting, we performed Data Augmentation techniques and we saw the accuracy increase to ```96.18%``` from ```86.93%```. Due to the imbalance of our data, we performed a stratified sampling of our data coupled with data augmentation so as not to decrease our training dataset. Our accuracy on a Mask dataset reaches ```99.84%``` after ```33``` hours of training. The real-time face recognition was a success and it is time to test the model with other people in the office at RT Knits.

The ```Data-Centric``` approach - holding the model fix and iteratively improving the quality of the data - seemed to be fruitful in the end. By constantly enhancing our dataset with data augmentation and a more fair sampling technique, it was possible to build a robust scalable model. About 80% of my time has been spent on ```data preparation```. Injecting more and more data to our model without a proper cleaning process or sampling technique or data augmentation process would never have created a good performing AI model. The Data-centric AI model was the key to building this face mask recognition model and more data processing will definitely improve our prediction accuracy. 
## References

1. https://arsfutura.com/magazine/face-recognition-with-facenet-and-mtcnn/
2. https://www.youtube.com/watch?v=0NSLgoEtdnw&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=36
3. https://www.youtube.com/watch?v=-FfMVnwXrZ0&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=32
4. https://www.youtube.com/watch?v=96b_weTZb2w&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=33
5. https://www.youtube.com/watch?v=6jfw8MuKwpI&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=34
6. https://www.youtube.com/watch?v=d2XB5-tuCWU&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=35
7. https://www.aiuai.cn/aifarm465.html
8. https://jonathan-hui.medium.com/ssd-object-detection-single-shot-multibox-detector-for-real-time-processing-9bd8deac0e06
9. https://medium.com/inveterate-learner/real-time-object-detection-part-1-understanding-ssd-65797a5e675b
10. https://github.com/davidsandberg/facenet
11. https://www.forbes.com/sites/gilpress/2021/06/16/andrew-ng-launches-a-campaign-for-data-centric-ai/?sh=5538affd74f5
12. https://docs.opencv.org/3.4/d4/d13/tutorial_py_filtering.html
13. https://www.geeksforgeeks.org/facenet-using-facial-recognition-system/
14. https://medium.com/analytics-vidhya/facenet-architecture-part-1-a062d5d918a1
15. https://towardsdatascience.com/a-simple-guide-to-the-versions-of-the-inception-network-7fc52b863202
16. https://www.geeksforgeeks.org/inception-v4-and-inception-resnets/
17. https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
18. http://llcao.net/cu-deeplearning17/pp/class10_FaceNet.pdf
19. https://www.geeksforgeeks.org/residual-networks-resnet-deep-learning/
20. https://www.geeksforgeeks.org/introduction-to-residual-networks/
21. https://www.youtube.com/watch?v=CNNnzl8HIIU&t=3425s
22. https://arxiv.org/abs/1512.03385
23. Aurelien Geron(2017): Hands-On Machine Learning with Scikit-Learn and TensorFlow

# face_recog_at_large_distance
# face_recog_at_large_distance
