<template>
  <div>
    <h2>My Orders</h2>
    <div v-for="order in orders" :key="order.id">
      <div>
        <h3>Order ID: {{ order.id }}</h3>
        <p>Customer: {{ order.customerName }}</p>
        <p>Quantity: {{ order.quantity }}</p>
        <p>Status: {{ order.status }}</p>
        
        <!-- Combined Button for PDF and Payment -->
        <button @click="downloadOrderDetails(order.id)">
          📄Download Order Details PDF & Initiate Payment
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      orders: [], // Array of orders
      paymentStatus: "", // To hold payment status
    };
  },
  methods: {
    async fetchOrders() {
      // Fetch orders from the backend
      try {
        const response = await this.$axios.get('/api/orders');
        this.orders = response.data;
      } catch (error) {
        console.error("Error fetching orders:", error);
      }
    },
    async downloadOrderDetails(orderId) {
      try {
        // Step 1: Generate PDF and initiate payment
        const response = await this.$axios.post('/api/order/payment', { orderId });
        
        // Step 2: Check payment response
        if (response.data.paymentInitiated) {
          this.paymentStatus = "Payment initiated successfully. Please proceed with the payment.";
          
          // Step 3: Trigger PDF download after successful payment initiation
          window.location.href = response.data.pdfDownloadUrl; // Download PDF
        } else {
          this.paymentStatus = "Payment initiation failed. Please try again.";
        }
      } catch (error) {
        console.error("Error initiating payment and generating PDF:", error);
        this.paymentStatus = "An error occurred during the process.";
      }
    },
  },
  created() {
    this.fetchOrders();
  },
};
</script>
