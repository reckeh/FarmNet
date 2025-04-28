<template>
  <div class="checkout-container">
    <h2>Checkout & Delivery Details</h2>

    <div class="checkout-content">
      <!-- Delivery Form -->
      <form @submit.prevent="placeOrder" class="checkout-form">
        <div class="form-group">
          <label for="recipientName">Recipient Name</label>
          <input type="text" v-model="recipientName" id="recipientName" placeholder="John Doe" required />
        </div>

        <div class="form-group">
          <label for="phoneNumber">Phone Number</label>
          <input type="text" v-model="phoneNumber" id="phoneNumber" placeholder="0712 345 678" required />
        </div>

        <div class="form-row">
          <div class="form-group half">
            <label for="deliveryCounty">County</label>
            <input type="text" v-model="deliveryCounty" id="deliveryCounty" placeholder="e.g. Nairobi" required />
          </div>

          <div class="form-group half">
            <label for="deliveryTown">Town</label>
            <input type="text" v-model="deliveryTown" id="deliveryTown" placeholder="e.g. Westlands" required />
          </div>
        </div>

        <div class="form-group">
          <label for="deliveryAddress">Delivery Address</label>
          <textarea v-model="deliveryAddress" id="deliveryAddress" placeholder="e.g. Apartment 4B, Riverside Lane" required></textarea>
        </div>

        <div class="form-group">
          <label for="deliveryNotes">Delivery Notes (Optional)</label>
          <textarea v-model="deliveryNotes" id="deliveryNotes" placeholder="Any instructions for the rider?"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group half">
            <label for="deliveryOption">Delivery Service</label>
            <select v-model="deliveryOption" id="deliveryOption" required>
              <option value="g4s">G4S</option>
              <option value="fargo">Fargo</option>
            </select>
          </div>

          <div class="form-group half">
            <label for="paymentMethod">Payment Method</label>
            <select v-model="paymentMethod" id="paymentMethod" required>
              <option value="mobileMoney">Mobile Money</option>
              <option value="creditCard">Credit Card</option>
            </select>
          </div>
        </div>

        <button type="submit" class="submit-btn">Place Order</button>
      </form>

      <!-- Order Summary -->
      <div class="checkout-summary">
        <h3>Order Summary</h3>
        <p><strong>Items:</strong> {{ cartItems.length }}</p>
        <p><strong>Total:</strong> <span class="total">KES {{ totalPrice.toLocaleString() }}</span></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recipientName: "",
      phoneNumber: "",
      deliveryCounty: "",
      deliveryTown: "",
      deliveryAddress: "",
      deliveryNotes: "",
      deliveryOption: "g4s",
      paymentMethod: "mobileMoney",
      cartItems: [],
      totalPrice: 0,
    };
  },
  mounted() {
    this.fetchCart();
  },
  methods: {
    placeOrder() {
      const token = localStorage.getItem("token");

      if (!token) return alert("Please log in first.");

      const payload = {
        recipient_name: this.recipientName,
        phone_number: this.phoneNumber,
        delivery_county: this.deliveryCounty,
        delivery_town: this.deliveryTown,
        delivery_address: this.deliveryAddress,
        delivery_notes: this.deliveryNotes,
        delivery_option: this.deliveryOption,
        payment_method: this.paymentMethod,
        cart_items: this.cartItems,
      };

      fetch("http://127.0.0.1:5000/checkout/place_order", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      })
        .then((res) => {
          if (!res.ok) throw new Error("Checkout failed");
          return res.json();
        })
        .then(() => {
          alert("Order placed successfully!");
          this.cartItems = [];
          this.totalPrice = 0;
          this.resetForm();
          this.$router.push({ name: "Orders" });
        })
        .catch((err) => {
          console.error("Checkout error:", err);
          alert("Failed to place order.");
        });
    },

    fetchCart() {
      const token = localStorage.getItem("token");

      fetch("http://127.0.0.1:5000/cart/cart", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.cart?.length) {
            this.cartItems = data.cart.map((item) => ({
              ...item,
              price: item.product_price || item.price,
            }));
            this.calculateTotalPrice();
          } else {
            this.cartItems = [];
          }
        })
        .catch((err) => {
          console.error("Fetch cart error:", err);
          alert("Failed to load cart.");
        });
    },

    calculateTotalPrice() {
      this.totalPrice = this.cartItems.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      );
    },

    resetForm() {
      this.recipientName = "";
      this.phoneNumber = "";
      this.deliveryCounty = "";
      this.deliveryTown = "";
      this.deliveryAddress = "";
      this.deliveryNotes = "";
      this.deliveryOption = "g4s";
      this.paymentMethod = "mobileMoney";
    },
  },
};
</script>

<style scoped>
.checkout-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fefefe;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.checkout-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

@media (min-width: 768px) {
  .checkout-content {
    flex-direction: row;
    align-items: flex-start;
  }
}

.checkout-form {
  flex: 2;
}

.checkout-summary {
  flex: 1;
  padding: 1rem;
  border-left: 1px solid #eee;
  background: #f9f9f9;
  border-radius: 8px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group.half {
  flex: 1;
}

label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

input,
textarea,
select {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #fff;
}

textarea {
  resize: vertical;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #28a745;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #218838;
}

.checkout-summary h3 {
  margin-bottom: 1rem;
}

.checkout-summary p {
  font-size: 16px;
  margin: 0.5rem 0;
}

.checkout-summary .total {
  font-size: 20px;
  color: #28a745;
  font-weight: bold;
}
</style>
