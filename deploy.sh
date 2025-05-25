#!/bin/bash

# Navigate to frontend directory
cd frontend

# Build the React app
npm run build

# Initialize git in build directory if not already initialized
cd build
if [ ! -d ".git" ]; then
git init
fi

# Add all files
git add .

# Commit changes
git commit -m "Update build"

# Push to gh-pages branch
git push -f https://github.com/EshwarDheekonda/OneMoat.git master:gh-pages
