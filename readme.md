# Minecraft Map Art

## Self Intro

Hello, this is the Automatic Chipmunk(my [bilibili](https://space.bilibili.com/513244188) username translation). You can simply call me Chipmunk :) (yes I love chipmunks)

## Project Info

the project aims to do a Minecraft Map Art generator

### Background Research

You can see quite a lot of Minecraft Map Art generator on the Internet, many of these tools use NBT to generate results.  
However, NBT requires you to stop the game and then use NBT.  
For servers, it's actually quite inconvenient, as stopping the server will decrease players' impression on the server.  
So we find the RCON protocol as an alt.  
The RCON protocol can enable remote minecraft command executing, which can also be used to generate Minecraft Map Art. 

## Notes about Usage

### Performance

We use "setblock" commands to place every block after analyzing the where to place the block. 
To show a picture, we need many pixels. For example, a picture of 256x144 means 36864 pixels (I know this is simple maths but aren't you amazed by such a small picture is displayed by more than thirty thousand pixels??)  
Which means that you should place 36864 blocks. Without special optimization, the server will receive 36864 "setblock" commands.  
So be sure that your server won't break!!!  
If you need a performance example, maybe I can consider adding a testing paragraph. 

## Contribution
You can do the following to contribute to this project
+ Write a GUI interface for main.py
+ Write a dictionary like the one in main.py, but mark the version of the game the dict is for
+ if you have some good idea, tell me 
### read before you do contribution
When you decide to do contribution, look if anyone has been working on the thing already, if not, announce in the issue about the thing you decide to do!  
Please update your process once every one week (update your process doesn't mean you need to do something every week, update is only used for "keep-alive" usage)
