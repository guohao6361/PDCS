FROM docker.1panel.live/library/eclipse-temurin:17-jdk-alpine

WORKDIR /app
COPY target/cart-service-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]