FROM docker.1ms.run/library/eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY target/product-service-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]