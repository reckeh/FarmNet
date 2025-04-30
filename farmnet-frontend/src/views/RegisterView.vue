<template>
  <div :style="containerStyle">
    <h2 :style="titleStyle">Register</h2>
    <form @submit.prevent="handleRegister" :style="formStyle">
      <!-- Username Input -->
      <input
        v-model="form.username"
        type="text"
        placeholder="Full Name"
        :style="inputStyle"
        required
      />
      <!-- Email Input -->
      <input
        v-model="form.email"
        type="email"
        placeholder="Email"
        :style="inputStyle"
        required
      />
      <!-- Password Input -->
      <div :style="passwordWrapperStyle">
        <input
          v-model="form.password"
          :type="passwordVisible ? 'text' : 'password'"
          placeholder="Password"
          :style="inputStyle"
          required
        />
        <span
          @click="togglePasswordVisibility"
          :style="eyeIconStyle"
          title="Toggle Password Visibility"
        >
          👁️
        </span>
      </div>
      <!-- Role Dropdown -->
      <select v-model="form.role" :style="inputStyle" required>
        <option disabled value="">Select Role</option>
        <option value="FARMER">Farmer</option>
        <option value="BUYER">Buyer</option>
        <option value="AGRI_EXPERT">Agricultural Expert</option>
        <option value="ADMIN">Admin</option>
      </select>
      
      <!-- Submit Button -->
      <button type="submit" :style="buttonStyle">Create Account</button>
    </form>

    <!-- Message Display -->
    <p v-if="message" :style="messageStyle">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        role: '', // Role selected from dropdown
      },
      passwordVisible: false, // Toggle state for password visibility
      message: '',
      containerStyle: {
        maxWidth: '400px',
        margin: '50px auto',
        padding: '30px',
        border: '1px solid #ccc',
        borderRadius: '12px',
        boxShadow: '0 0 10px rgba(0,0,0,0.1)',
        backgroundColor: '#fdfdfd',
      },
      titleStyle: {
        textAlign: 'center',
        marginBottom: '20px',
        fontSize: '24px',
      },
      formStyle: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
      },
      inputStyle: {
        padding: '10px',
        borderRadius: '6px',
        border: '1px solid #ccc',
      },
      buttonStyle: {
        padding: '10px',
        backgroundColor: '#007BFF',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
      },
      messageStyle: {
        marginTop: '15px',
        color: 'green',
        textAlign: 'center',
      },
      passwordWrapperStyle: {
        display: 'flex',
        alignItems: 'center',
        position: 'relative',
      },
      eyeIconStyle: {
        position: 'absolute',
        right: '10px',
        cursor: 'pointer',
        fontSize: '18px',
      },
    };
  },
  methods: {
    // Toggle password visibility
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },

    // Handle form submission for registration
    async handleRegister() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/auth/register", this.form);
        this.message = response.data.message || "Registration successful!";
        this.form.username = '';
        this.form.email = '';
        this.form.password = '';
        this.form.role = ''; 
      } catch (error) {
        this.message = error.response?.data?.message || "Registration failed.";
      }
    },
  },
};
</script>
