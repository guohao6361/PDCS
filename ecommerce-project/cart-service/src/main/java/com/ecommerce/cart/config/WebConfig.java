package com.ecommerce.cart.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private JwtAuthFilter jwtAuthFilter;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }

    @Bean
    public FilterRegistrationBean<JwtAuthFilter> jwtFilter() {
        FilterRegistrationBean<JwtAuthFilter> registrationBean = new FilterRegistrationBean<>();
        registrationBean.setFilter(jwtAuthFilter);
        registrationBean.addUrlPatterns("/cart/*");
        registrationBean.setOrder(1);
        return registrationBean;
    }
}
