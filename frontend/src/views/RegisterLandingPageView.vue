<template>
  <PageHeadingWithDescription
    pageTitle="Register for a RASDS account"
    pageDescription="There are two types of user roles in the RASDS - Data Requestor and Data Custodian.
  If you or your organisation doesn't manage any restricted access species datasets and you are just wanting
  to be able to request access to these datasets, please register as a data requestor." />
  <div class="container">
    <section class="section">
      <div class="level py-6 my-3 px-6">
        <div class="has-text-centered">
          <RouterLink :to="{ name: 'register-data-requestor' }">
            <o-button
              variant="primary"
              class="extra-large is-size-3-desktop py-6-desktop is-size-3-touch is-size-4-mobile py-4-mobile">
              Register as a Data Requestor
            </o-button>
          </RouterLink>
          <p class="pb-5 pt-2 mx-5 mb-5">If you are not a data custodian, choose this option</p>
        </div>
        <div class="has-text-centered">
          <RouterLink :to="{ name: 'register-data-custodian' }">
            <o-button
              variant="primary"
              class="extra-large is-size-3-desktop py-6-desktop is-size-3-touch is-size-4-mobile">
              Register as a Data Custodian
            </o-button>
          </RouterLink>
          <p class="pb-5 pt-2 mx-5 mb-5">As a data custodian, you qualify also to request data</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import PageHeadingWithDescription from '../components/PageHeadingWithDescription.vue';

export default {
  components: {
    PageHeadingWithDescription,
  },
};
</script>

<style scoped>
.extra-large {
  padding-top: 5rem;
  padding-bottom: 5rem;
}
</style>
