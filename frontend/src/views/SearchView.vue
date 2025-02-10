<template>
  <PageHeadingWithDescription
    pageTitle="Metadata Search"
    pageDescription="The Restricted Access Species Data Service provides a discovery and request tracking service for Restricted Access Species Data.
    Once you have logged in, you can request access to up to ten datasets. Complete the data access request form, to contact the relevant data custodian/s to grant access to the datasets you have selected." />
  <div class="container">
    <div class="section">
      <div v-if="showRequestForm" class="columns">
        <div class="column is-align-content-end">
          <DataAccessRequest
            :metadata-ids="selectedResults"
            :access-values="this.accessValues"
            :industryClassification-values="this.industryClassificationValues"
            :purpose-values="this.purposeValues"
            :researchClassification-values="this.researchClassificationValues"
            @back="backClicked" />
        </div>
      </div>
      <div v-if="!showRequestForm" class="columns">
        <div class="column">
          <div class="card">
            <div class="card-content">
              <p class="title">Filters</p>
              <div class="content">
                <div class="field">
                  <o-field class="label">Keywords:</o-field>
                  <o-dropdown expanded v-if="keywordsOptions" v-model="keywords" multiple role="list">
                    <template #trigger>
                      <o-button variant="primary" type="button">
                        <span v-if="keywords.length > 0">
                          {{ keywords.slice(0, 4).join(', ').toString() }}
                          <span v-if="keywords.length > 4">...</span>
                        </span>
                        <span v-else> Please select keywords </span>
                      </o-button>
                    </template>
                    <o-dropdown-item v-for="keyword in keywordsOptions" :value="keyword">{{ keyword }}</o-dropdown-item>
                  </o-dropdown>
                </div>
                <o-field label="Title:">
                  <o-input v-model="title"> </o-input>
                </o-field>
                <o-field label="Description:">
                  <o-input v-model="description"></o-input>
                </o-field>
                <div class="field">
                  <o-field class="label">Locations:</o-field>
                  <o-dropdown expanded v-if="locationsOptions" v-model="locations" multiple role="list">
                    <template #trigger>
                      <o-button variant="primary" type="button">
                        <span v-if="locations.length > 0">
                          {{ locations.slice(0, 3).join(', ') }}
                          <span v-if="locations.length > 3">...</span>
                        </span>
                        <span v-else>Please select locations</span>
                      </o-button>
                    </template>
                    <o-dropdown-item v-for="location in locationsOptions" :value="location" :key="location">{{
                      location
                    }}</o-dropdown-item>
                  </o-dropdown>
                </div>
                <o-field label="Data Custodian">
                  <o-autocomplete
                    v-if="organisationOptions"
                    v-model="organisations"
                    expanded
                    placeholder="e.g. CSIRO"
                    clearable
                    :data="filteredOrganisationsObj"
                    field="name"
                    @select="(option) => (this.selectedOrg = option)">
                    <template #empty>No results found</template>
                  </o-autocomplete>
                </o-field>
                <div class="buttons is-justify-content-space-between mt-5">
                  <o-button @click="onClickSearch" variant="secondary">
                    <span>Apply Filter(s)</span>
                  </o-button>
                  <o-button @click="clearFilters" variant="edit">
                    <span>Clear Filter(s)</span>
                  </o-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-two-thirds">
          <div class="is-flex is-justify-content-space-between w-full">
            <div>
              <o-button
                icon-pack="fas"
                @click="this.page = this.page - 1"
                class="nav-previous"
                :disabled="this.page === 0 || searchResults.results.length === 0"
                aria-label="previous-page"
                ><font-awesome-icon icon="fa-solid fa-angle-left"
              /></o-button>
              <o-button
                icon-pack="fas"
                @click="this.page = this.page + 1"
                class="nav-next"
                :disabled="final_page || searchResults.results.length === 0"
                aria-label="next-page"
                ><font-awesome-icon icon="fa-solid fa-angle-right"
              /></o-button>
            </div>
            <div v-if="searchResults.results.length > 0">
              <o-button
                :variant="isSelecting ? 'danger' : 'info'"
                type="button"
                @click="toggleIsSelecting"
                :disabled="!canRequest">
                {{ isSelecting ? 'Cancel' : 'Select multiple (Max 10)' }}
              </o-button>
              <o-button
                v-if="selectedResults.length > 0"
                variant="primary"
                type="button"
                class="ml-2"
                @click="showRequestForm = true">
                Request data {{ selectedResults.length > 0 ? `(${selectedResults.length}) (Max 10)` : '' }}
              </o-button>
            </div>
          </div>
          <div class="mt-4" v-for="result in searchResults.results" :key="result.id">
            <div class="card mb-4">
              <div class="card-content">
                <div class="content">
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-book" />
                      </span>
                      <span class="has-text-weight-bold">Title:</span>
                    </span>
                    {{ result.title }}
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-file-lines" />
                      </span>
                      <span class="has-text-weight-bold">Description:</span>
                    </span>
                    {{ result.abstract }}
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-location-dot" />
                      </span>
                      <span class="has-text-weight-bold">Locations:</span>
                    </span>
                    {{ result.locations.join(', ') }}
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-building" />
                      </span>
                      <span class="has-text-weight-bold">Data Custodian:</span>
                    </span>
                    {{ result.custodian }}
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-tag" />
                      </span>
                      <span class="has-text-weight-bold">Keywords:</span>
                    </span>
                    {{ result.keywords.join(', ') }}
                  </p>
                  <div class="is-flex is-justify-content-end">
                    <o-button
                      :variant="selectButtonClass(result.id)"
                      type="button"
                      @click="isSelecting ? onSelect(result.id) : requestSingle(result.id)"
                      :disabled="!canRequest">
                      {{ selectButtonText(result.id) }}
                    </o-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="searchResults.results.length === 0"
            class="is-flex has-text-justified-center is-size-5 has-text-weight-semibold">
            <p>
              There are no results for your search criteria. Try searching by Title or Description using specific terms
              expected.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import PageHeadingWithDescription from '../components/PageHeadingWithDescription.vue';
import {
  getKeywordsAPI,
  getLocationsAPI,
  getMetadataSearchAPI,
  getOrganisationsAPI,
  lookupAccessRequestEnumAPI,
} from '@/api/api';
import DataAccessRequest from '@/views/DataAccessRequest.vue';
import { defineComponent } from 'vue';
import { AccessRequestEnumType } from '@/api/api.types';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { useUserDataStore } from '@/store';

export default defineComponent({
  components: {
    DataAccessRequest,
    PageHeadingWithDescription,
  },
  beforeMount() {
    this.getOptions();
    this.getSearch();
    lookupAccessRequestEnumAPI(AccessRequestEnumType.Accesses).then(({ data }) => (this.accessValues = data || []));
    lookupAccessRequestEnumAPI(AccessRequestEnumType.IndustryClassifications).then(
      ({ data }) => (this.industryClassificationValues = data || [])
    );
    lookupAccessRequestEnumAPI(AccessRequestEnumType.Purposes).then(({ data }) => (this.purposeValues = data || []));
    lookupAccessRequestEnumAPI(AccessRequestEnumType.ResearchClassifications).then(
      ({ data }) => (this.researchClassificationValues = data || [])
    );
    const userStore = useUserDataStore();
    this.canRequest = userStore.isLoggedIn;
  },
  data() {
    return {
      title: '',
      description: '',
      organisations: '',
      cursor: '',
      selectedOrg: null,
      previousCursors: [''],
      page: 0,
      finalPageHit: false,
      searchStarted: false,
      keywords: [],
      keywordsOptions: [],
      locations: [],
      locationsOptions: [],
      organisationOptions: [],
      searchResults: {
        results: [],
      },
      filteredOrganisationsObj: [],
      loading: false,
      isSelecting: false,
      selectedResults: [] as string[],
      showRequestForm: false,
      // These are defined in the enums, but loading them from the API is low hanging fruit for added resilience
      custodianValues: [] as string[],
      requestorValues: [] as string[],
      accessValues: [] as string[],
      areaValues: [] as string[],
      frequencyValues: [] as string[],
      industryClassificationValues: [] as string[],
      purposeValues: [] as string[],
      researchClassificationValues: [] as string[],
      canRequest: false,
    };
  },
  watch: {
    page(newPage, oldPage) {
      if (newPage > oldPage) {
        if (!this.finalPageHit || !this.previousCursors.includes(this.searchResults['cursor'])) {
          this.previousCursors.push(this.searchResults['cursor']);
        }
        this.getSearch(this.searchResults['cursor']);
        if (this.final_page) {
          this.finalPageHit = true;
        }
      } else {
        this.getSearch(this.previousCursors[newPage]);
      }
    },
    filteredOrganisations(newFilteredOrganisationsObj) {
      this.filteredOrganisationsObj = newFilteredOrganisationsObj;
    },
  },
  computed: {
    final_page() {
      return this.searchResults['cursor'] === null;
    },
    filteredOrganisations() {
      return this.organisationOptions.filter(
        (option) => option.name.toLowerCase().indexOf(this.organisations.toLowerCase()) >= 0
      );
    },
  },
  methods: {
    async getOptions() {
      this.loading = true;
      this.keywordsOptions = await getKeywordsAPI();
      this.locationsOptions = await getLocationsAPI();
      this.organisationOptions = await getOrganisationsAPI();
      this.loading = false;
    },
    async getSearch(pageCursor = '') {
      this.loading = true;
      this.searchResults = await getMetadataSearchAPI(
        20,
        pageCursor,
        this.keywords,
        this.locations,
        this.title,
        this.description,
        this.selectedOrg ? this.selectedOrg.id : ''
      );
      this.loading = false;
    },
    onClickSearch() {
      this.previousCursors = [''];
      this.finalPageHit = false;
      this.page = 0;
      this.getSearch();
    },
    clearFilters() {
      this.page = 0;
      this.title = '';
      this.description = '';
      this.organisations = '';
      this.locations = [];
      this.keywords = [];
      this.selectedOrg = null;
      this.previousCursors = [''];
      this.finalPageHit = false;
      this.getSearch('');
    },
    resultIsSelected(id: string): boolean {
      return this.selectedResults.indexOf(id) >= 0;
    },
    onSelect(id: string) {
      const { oruga } = useProgrammatic();
      if (this.resultIsSelected(id)) {
        this.selectedResults = this.selectedResults.filter((result) => result !== id);
      } else {
        if (this.selectedResults.length >= 10) {
          return oruga.notification.open({
            message:
              'You may only have 10 results selected at one time. Please remove a result from your selections before continuing to add more.',
            position: 'top',
            closable: true,
            variant: 'danger',
            duration: 10000,
          });
        }
        this.selectedResults.push(id);
      }
    },
    selectButtonText(id: string): string {
      let text: string;
      if (this.isSelecting && this.resultIsSelected(id)) {
        text = 'Deselect';
      } else if (this.isSelecting) {
        text = 'Select';
      } else {
        text = 'Request data';
      }
      return text;
    },
    selectButtonClass(id: string): 'primary' | 'success' | 'danger' {
      let buttonClass: string = 'primary';
      if (this.isSelecting && this.resultIsSelected(id)) {
        buttonClass = 'danger';
      } else if (this.isSelecting) {
        buttonClass = 'success';
      }
      return buttonClass;
    },
    toggleIsSelecting() {
      this.selectedResults = [];
      this.isSelecting = !this.isSelecting;
    },
    requestSingle(id: string) {
      this.selectedResults = [id];
      this.showRequestForm = true;
    },
    backClicked(clearResults: boolean = false) {
      this.$router.push('');
      if (clearResults) {
        this.selectedResults = [];
        this.isSelecting = false;
      }
      this.showRequestForm = false;
    },
  },
});
</script>
<style lang="scss">
.button.nav-previous {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.button.nav-next {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
</style>
