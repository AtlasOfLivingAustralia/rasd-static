<template>
  <PageHeading pageTitle="Forgot password" />
  <div class="container">
    <div class="section">
      <o-field label="Username">
        <o-input
          type="email"
          id="username"
          v-model="username"
          placeholder="Your work email address"
          maxlength="200"></o-input>
      </o-field>
      <div class="mt-4 mb-4 container is-flex is-justify-content-space-between is-align-items-center">
        <o-button
          :disabled="this.loading"
          :class="{ 'is-loading': this.loading }"
          type="submit"
          variant="primary"
          class="button"
          @click="forgotPassword"
          >Forgot password</o-button
        >
        <router-link class="mt-4" to="login">Back to login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { forgotPasswordAPI } from '../api/api';

export default {
  components: {
    PageHeading,
  },
  data() {
    return {
      username: '',
      loading: false,
    };
  },
  methods: {
    async forgotPassword() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await forgotPasswordAPI(this.username);
      this.loading = false;
      oruga.notification.open({
        message: this.notification[0],
        position: 'top',
        closable: true,
        duration: 10000,
        variant: this.notification[1] ? 'success' : 'danger',
      });
      if (this.notification[1]) {
        this.$router.beforeEach((to) => {
          to.meta.username = this.username;
        });
        this.$router.push('/forgot-password/confirm');
      } else {
        this.username = '';
      }
    },
  },
};
</script>

<style scoped></style>
