# The first thing we need to do is define from what image we want to build from. Here we will use the
# latest LTS (long term support) version 14 of node available from the Docker Hu
FROM node:14

# Environmet Variables
ENV NODE_ENV=dev
ENV PORT=3000

# Bundle app source
# To bundle your app's source code inside the Docker image, use the COPY instruction
COPY . /app
# create a directory to hold the application code inside the image, this will be the working directory for your application:
WORKDIR /app

# Install app dependencies
RUN npm install

# Your app binds to port $PORT so you'll use the EXPOSE instruction to have it mapped by the docker daemon
EXPOSE $PORT
# Last but not least, define the command to run your app using CMD which defines your runtime.
# Here we will use npm start to start app
ENTRYPOINT ["npm", "start"]
