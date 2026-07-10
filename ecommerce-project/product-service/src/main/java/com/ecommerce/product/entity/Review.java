package com.ecommerce.product.entity;

import jakarta.validation.constraints.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "reviews")
public class Review {

    @Id
    private String id;

    @NotNull(message = "商品ID不能为空")
    private Integer productId;

    @NotBlank(message = "用户名不能为空")
    private String username;

    @NotBlank(message = "评价内容不能为空")
    private String content;

    @NotNull(message = "评分不能为空")
    @Min(value = 1, message = "评分最低为1")
    @Max(value = 5, message = "评分最高为5")
    private Integer rating;

    // 手动 Getter & Setter
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public Integer getProductId() { return productId; }
    public void setProductId(Integer productId) { this.productId = productId; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }
}