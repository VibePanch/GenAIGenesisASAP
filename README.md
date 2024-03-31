# GenAIGenesisASAP

Requirements:
-Raspberry Pi
-Ultrasonic Sensor
-Headphones
Plus any software requirements 

Our design is inspired by echolocation/use of hearing commonly used by visually impaired individuals in some form. Our team sought to create a more streamlined and intuitive solution exceeding the efficiency of these methods. 

ASAP takes the distance between the user and nearby obstacles and plays a soft periodic sound at the same time. This sound will increase in noise level when the user travels closer to an obstacle. When the user reaches a threshold distance to the obstacle, the device will play an audible warning describing the obstacle and requesting the user to stop moving. 

We built it using a raspberry pi microprocessor as the brain and controller of the project. It makes use of an ultrasonic sensor, voltage divider circuits, webcams, and headphones, to create the sensory input and output for the ASAP. Using mongoDB as our database we were able to communicate the sensory data to the server and take the computed and analyzed result from the google gemini ai result to the ASAP client side, where using audio interfacing, mixing and output, the ASAP conveys audio data of their surroundings and any potential hazards in proximity through text-to-speech and other audio cues.

We had hardware challenges at the start with using the Raspberry pi, do to a lack of a monitor making it hard to use the raspberry pi, but we found the workaround to this using VNC. We also had several software issues with the raspberry pi because its OS and software requirements were very outdated and needed to be updated. On the server side, the initial setup of Google Cloud and Gemini took a good bit of effort to make work, which later turned to more difficulties when we accidentally used up all the credits in an infinite loop, so we had to swap accounts. Overall, through the challenges we learned many things about the different technologies we worked with to make this project happen and had a chance to learn all the intricacies that make them work.

Our team is extremely proud of completing a proper prototype for this project. The use of multimodal inputs and outputs as well as multithreading proved to be a significant challenge that our team overcame. 

Our team hopes to scale the size of ASAP down from helmets to wearable glasses. 
