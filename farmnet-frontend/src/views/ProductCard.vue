<template>
    <div class="product-card" style="border: 1px solid #eee; border-radius: 10px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
      <img :src="product.image_url" alt="Product" style="width: 100%; height: 180px; object-fit: cover; border-radius: 8px;" />
      <h3 style="font-weight: 600; margin-top: 10px;">{{ product.name }}</h3>
      <p style="font-size: 14px; color: #555;">{{ product.description }}</p>
      <p style="font-weight: bold; color: #2e7d32;">{{ product.price }} KES / {{ product.unit }}</p>
      <button @click="addToCart" style="margin-top: 10px; padding: 8px 12px; background-color: #ff6600; color: #fff; border: none; border-radius: 5px; cursor: pointer;">
        Add to Cart
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "ProductCard",
    props: ["product"],
    methods: {
      addToCart() {
        const cart = JSON.parse(localStorage.getItem("cart")) || [];
        const itemIndex = cart.findIndex(p => p.id === this.product.id);
        if (itemIndex !== -1) {
          cart[itemIndex].quantity += 1;
        } else {
          cart.push({ ...this.product, quantity: 1 });
        }
        localStorage.setItem("cart", JSON.stringify(cart));
        alert("Added to cart!");
      }
    }
  };
  </script>
  