FROM oven/bun:1 as base

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and the bun.lockb files
COPY package.json bun.lockb ./

# Install dependencies
RUN bun install

# Copy the rest of the application code
COPY . .

# Build the app
RUN bun run build

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["bun", "run", "start"]
