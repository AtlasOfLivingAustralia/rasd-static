<script lang="ts">
import { defineComponent } from 'vue';
import { getAccessRequestsPublicAPI } from '@/api/api';
import { DateTime } from 'luxon';
import PageHeading from '../components/PageHeading.vue';

export default defineComponent({
  name: 'PublicDARView',
  components: { PageHeading },
  beforeMount() {
    this.getDataAccessRequest();
  },
  data() {
    return {
      loading: false,
      created_at: '',
      doi: '',
      data_frequency: '',
      data_frequency_explanation: '',
      data_required_from: '',
      data_required_to: '',
      data_area: '',
      data_area_explanation: '',
      completed_at: '',
      data_requested: null,
    };
  },
  computed: {
    formattedHeading() {
      return `RASDS Data Access Request created on ${this.created_at}`;
    },
  },
  methods: {
    async getDataAccessRequest() {
      this.loading = true;
      const accessRequest = await getAccessRequestsPublicAPI(this.$route.params.id);
      console.log(accessRequest.data.result);
      this.created_at = accessRequest?.data.result.created_at
        ? DateTime.fromISO(accessRequest?.data.result.created_at).setLocale('en-AU').toLocaleString()
        : null;
      this.doi = accessRequest?.data.result.doi;
      this.data_frequency = accessRequest?.data.result.data_frequency;
      this.data_frequency_explanation = accessRequest?.data.result.data_frequency_explanation;
      this.data_required_from = accessRequest?.data.result.data_required_from
        ? DateTime.fromISO(accessRequest?.data.result.data_required_from).setLocale('en-AU').toLocaleString()
        : null;
      this.data_required_to = accessRequest?.data.result.data_required_to
        ? DateTime.fromISO(accessRequest?.data.result.data_required_to).setLocale('en-AU').toLocaleString()
        : null;
      this.data_area = accessRequest?.data.result.data_area;
      this.data_area_explanation = accessRequest?.data.result.data_area_explanation;
      this.completed_at = accessRequest?.data.result.completed_at
        ? DateTime.fromISO(accessRequest?.data.result.completed_at).setLocale('en-AU').toLocaleString()
        : null;
      this.data_requested = accessRequest?.data.result.data_requested;
      this.loading = false;
    },
  },
});
</script>

<template>
  <PageHeading :pageTitle="this.formattedHeading" />
  <div class="container">
    <div class="section">
      <div>
        <p v-if="doi"><strong>DOI:</strong> {{ doi }}</p>
        <p><strong>Data Frequency:</strong> {{ data_frequency }}</p>
        <p v-if="data_required_from"><strong>Data Required From:</strong> {{ data_required_from }}</p>
        <p v-if="data_required_to"><strong>Data Required To:</strong> {{ data_required_to }}</p>

        <p><strong>Data Area:</strong> {{ data_area }}</p>
        <p><strong>Data Area Explanation:</strong> {{ data_area_explanation }}</p>
        <p><strong>Created At:</strong> {{ created_at }}</p>

        <p v-if="completed_at"><strong>Completed At:</strong> {{ completed_at }}</p>
        <p><strong>Update Frequency:</strong> {{ data_frequency }}</p>
        <p v-if="data_frequency_explanation">
          <strong>Data Frequency Explanation:</strong> {{ data_frequency_explanation }}
        </p>

        <div>
          <strong>Data Requested:</strong>
          <div :key="key" v-for="(data_request, key) in data_requested">
            <div class="box">
              <p><strong>Metadata Title:</strong> {{ data_request.metadataTitle }}</p>
              <p><strong>Custodian Name:</strong> {{ data_request.custodianName }}</p>
              <p v-if="data_request.data_source_doi">
                <strong>Data Source DOI:</strong> {{ data_request.data_source_doi }}
              </p>
              <p v-if="data_request.data_source_url">
                <strong>Data Source URL:</strong> {{ data_request.data_source_url }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
