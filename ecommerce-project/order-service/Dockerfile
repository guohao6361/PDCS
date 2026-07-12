FROM docker.1ms.run/library/eclipse-temurin:17-jdk-alpine
LABEL maintainer="ecommerce-team"
WORKDIR /app
COPY target/order-service-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8084
ENV JAVA_OPTS="-Xmx256m -Xms128m -Duser.timezone=Asia/Shanghai"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8084/actuator/health || exit 1
