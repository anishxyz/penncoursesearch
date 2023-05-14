# /penncoursesearch/frontend/Dockerfile

# Use an official Node.js runtime as a parent image
FROM node:19

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in package.json
RUN npm install

# Build the app for production
RUN npm run build

# Expose port 3000 for the app
EXPOSE 3000

# Serve the app using serve package
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
