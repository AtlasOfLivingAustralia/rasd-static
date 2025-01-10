<template>
  <PageHeadingWithDescription
    pageTitle="About"
    pageDescription="The Restricted Access Species Data Service (RASDS) was developed as part of a collaborative project (the Restricted Access Species Data Project) between the Atlas of Living Australia, Australian Research Data Commons (ARDC), Australian Government, state and territory conservation agencies, museums, and herbaria, EcoCommons and the Western Australian Biodiversity Science Institute. " />
  <div class="container">
    <section class="section">
      <h3 class="is-size-3">What does the RASDS do?</h3>
      <p class="has-text-justified pb-6">
        The service aims to provide a single place for users to discover and request Australian restricted access
        species data. The service enables data custodians and data requestors to track the progress of and manage their
        requests. Data custodians can also track the use of their data via a digital object identifier (DOI) through the
        service.
      </p>

      <h3 class="is-size-3">Who is the RASDS for?</h3>
      <p class="has-text-justified pb-6">
        Data custodians who choose to opt into the service will use the service to track and manage requests for
        restricted access species data that the data custodians hold. Users who want to access full-resolution
        restricted access species data can use the service to request this data from one or multiple data custodians.
      </p>

      <h3 class="is-size-3">Things to note:</h3>
      <div class="content has-text-justified">
        <ul class="pb-6 mt-0">
          <li>The custodianship of the data always remains with the data providers.</li>
          <li>
            The data service is not intended to replace existing state and territory processes for requesting data,
            however it aims to streamline user requests covering multiple datasets.
          </li>
          <li>
            The service will neither transfer nor store species data. It is simply a request workflow and tracking
            system to support data requestors and data custodians.
          </li>
        </ul>
        <p class="has-text-justified">
          For further information about the data service or the framework, please email us on
          <a href="mailto:info@rasd.org.au">info@rasd.org.au.</a>
        </p>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import PageHeadingWithDescription from '../components/PageHeadingWithDescription.vue';
export default {
  components: {
    PageHeadingWithDescription,
  },
};
</script>

<style scoped></style>
