<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>

    <!-- Section: User Management -->
    <section class="users-section">
      <h2>Users</h2>
      <form @submit.prevent="handleUserSubmit">
        <input v-model="userForm.name" placeholder="Name" required />
        <input v-model="userForm.email" placeholder="Email" required />
        <input v-model="userForm.role" placeholder="Role" required />
        <input v-model="userForm.password" placeholder="Password" required />
        <button type="submit">{{ editingUserId ? 'Update' : 'Add' }}</button>
      </form>

      <ul>
        <li v-for="user in users" :key="user.id">
          <div v-for="(value, key) in user" :key="key" v-if="key !== 'password'">
            <strong>{{ key }}:</strong> {{ value }}
          </div>
          <button @click="editUser(user)">Edit</button>
          <button @click="deleteUser(user.id)">Delete</button>
          <hr />
        </li>
      </ul>
    </section>

    <!-- Section: Usage Logs -->
    <section class="usage-section">
      <h2>System Usage</h2>
      <p><strong>Total Logins:</strong> {{ usage.totalLogins }}</p>
      <p><strong>Active Sessions:</strong> {{ usage.activeSessions }}</p>
      <ul>
        <li v-for="log in usage.logs" :key="log.id">
          {{ log.user }} - {{ log.action }} @ {{ log.date }}
        </li>
      </ul>
    </section>

    <!-- Section: Reports -->
    <section class="reports-section">
      <h2>Reports</h2>
      <p><strong>Total Users:</strong> {{ reports.totalUsers }}</p>
    </section>

    <!-- Button to download the PDF of user actions -->
    <button @click="generatePDF">User Actions PDF</button>
  </div>
</template>

<script>
import axios from 'axios';
import { jsPDF } from "jspdf";

const BASE_URL = 'http://127.0.0.1:5000'; // Flask backend

export default {
  name: 'AdminDashboard',
  data() {
    return {
      users: [],
      usage: {
        totalLogins: 0,
        activeSessions: 0,
        logs: []
      },
      reports: {
        totalUsers: 0
      },
      userForm: {
        name: '',
        email: '',
        role: '',
        password: ''
      },
      editingUserId: null
    };
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('token');
      return {
        Authorization: `Bearer ${token}`
      };
    },
    async fetchUsers() {
      try {
        const res = await axios.get(`${BASE_URL}/users/`, {
          headers: this.getAuthHeaders()
        });
        this.users = res.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async fetchUsage() {
      try {
        const res = await axios.get(`${BASE_URL}/pattern/pattern`, {
          headers: this.getAuthHeaders()
        });
        this.usage = res.data;
      } catch (error) {
        console.error('Error fetching usage:', error);
      }
    },
    async fetchReports() {
      try {
        const res = await axios.get(`${BASE_URL}/reports/reports/total_users`, {
          headers: this.getAuthHeaders()
        });
        this.reports = res.data;
      } catch (error) {
        console.error('Error fetching reports:', error);
      }
    },
    async handleUserSubmit() {
      try {
        if (this.editingUserId) {
          await axios.put(`${BASE_URL}/users/${this.editingUserId}`, this.userForm, {
            headers: this.getAuthHeaders()
          });
        } else {
          await axios.post(`${BASE_URL}/users/`, this.userForm, {
            headers: this.getAuthHeaders()
          });
        }
        this.resetForm();
        this.fetchUsers();
      } catch (error) {
        console.error('Error submitting user form:', error);
      }
    },
    editUser(user) {
      this.userForm = {
        name: user.name,
        email: user.email,
        role: user.role,
        password: ''
      };
      this.editingUserId = user.id;
    },
    async deleteUser(id) {
      try {
        await axios.delete(`${BASE_URL}/users/${id}`, {
          headers: this.getAuthHeaders()
        });
        this.fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    resetForm() {
      this.userForm = { name: '', email: '', role: '', password: '' };
      this.editingUserId = null;
    },
    generatePDF() {
      const doc = new jsPDF();
      doc.text('User Actions Log', 20, 20);
      let yPosition = 30;
      
      this.usage.logs.forEach(log => {
        doc.text(`${log.user} - ${log.action} @ ${log.date}`, 20, yPosition);
        yPosition += 10; 
      });

      doc.save('user-actions-log.pdf');
    }
  },
  mounted() {
    this.fetchUsers();
    this.fetchUsage();
    this.fetchReports();

    setInterval(() => {
      this.fetchUsage();
      this.fetchReports();
    }, 1200000); 
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  max-width: 800px;
  margin: auto;
}
section {
  margin-bottom: 2rem;
}
input {
  margin: 0.2rem;
}
button {
  margin-left: 0.5rem;
}
</style>
