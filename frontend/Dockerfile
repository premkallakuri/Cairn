FROM node:22-alpine

WORKDIR /workspace/frontend

COPY package.json ./
RUN npm install -g pnpm && pnpm install

COPY . .

EXPOSE 3000

CMD ["pnpm", "dev", "--hostname", "0.0.0.0", "--port", "3000"]
