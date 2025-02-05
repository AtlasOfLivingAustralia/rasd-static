<template>
  <PageHeading pageTitle="Reset password" />
  <div class="container">
    <div class="section">
      <o-field label="Your email address:">
        <o-input type="email" value="email" maxlength="200"></o-input>
      </o-field>
      <div class="mt-4 mb-4 container is-flex is-justify-content-space-between is-align-items-center">
        <o-button type="submit" class="button">Reset password</o-button>
        <router-link class="mt-4" to="login">Back to login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';

export default {
  components: {
    PageHeading,
  },
};
</script>

<style scoped></style>
