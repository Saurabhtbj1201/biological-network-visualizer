FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build for development (watch mode)
ENV VITE_API_BASE_URL=http://localhost:5000/api

EXPOSE 3000

CMD ["npm", "run", "dev"]
