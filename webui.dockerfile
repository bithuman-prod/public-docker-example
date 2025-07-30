FROM node:18-alpine

WORKDIR /app

# Install git for cloning
RUN apk add --no-cache git

# Clone the LiveKit agents playground frontend
RUN git clone https://github.com/bithuman-prod/public-livekit-ui-example.git .

# Install dependencies
RUN npm cache clean --force && \
    npm install --force

# Set LiveKit connection URL
ARG LIVEKIT_URL
ENV NEXT_PUBLIC_LIVEKIT_URL=$LIVEKIT_URL
ENV LIVEKIT_URL=$LIVEKIT_URL

# Build the application
RUN npm run build

# Set production environment
ENV NODE_ENV=production

# Expose port 3000 (Next.js default)
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 