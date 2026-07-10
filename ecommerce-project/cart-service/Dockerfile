FROM eclipse-temurin:17-jre-alpine
LABEL maintainer="ecommerce-team"
WORKDIR /app
COPY target/cart-service-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8083
ENV JAVA_OPTS="-Xmx256m -Xms128m"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8083/actuator/health || exit 1
FROM docker.1panel.live/library/eclipse-temurin:17-jdk-alpine

WORKDIR /app
COPY target/cart-service-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]