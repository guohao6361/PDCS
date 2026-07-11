package com.ecommerce.common;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 标记内部服务间调用端点，跳过 JWT 鉴权。
 * 仅限微服务网络内部调用，不应暴露给外部客户端。
 */
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface InternalApi {
}
