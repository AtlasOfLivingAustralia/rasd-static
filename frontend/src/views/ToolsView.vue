<template>
  <div v-if="isLoggedIn">
    <PageHeadingWithDescription
      :pageTitle="`${organisationName}`"
      :pageDescription="`ABN ${organisationABN}`"
      :extraDescription="`${organisationEmail}`" />
    <div class="container">
      <section class="section pt-6">
        <div v-if="isAdministrator" class="section pt-0 pb-4">
          <h2 class="is-size-3">Admin Tools</h2>
          <div class="column is-three-quarters">
            <div class="card mb-4">
              <div class="card-content">
                <div class="content">
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-list-ul" />
                      </span>
                      <span class="tools-link">
                        <router-link :to="{ name: 'assess-organisation-requests' }">
                          Registration Requests
                        </router-link>
                      </span>
                    </span>
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-people-roof" />
                      </span>
                      <span class="tools-link">
                        <router-link :to="{ name: 'organisations' }"> Manage Organisations </router-link>
                      </span>
                    </span>
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-list-alt" />
                      </span>
                      <span class="tools-link">
                        <router-link :to="{ name: 'metadata-list' }"> View RASD Metadata </router-link>
                      </span>
                    </span>
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-clipboard-list" />
                      </span>
                      <span class="tools-link">
                        <router-link :to="{ name: 'data-access-request-admin' }">
                          All Data Access Requests
                        </router-link>
                      </span>
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="isAdministrator || isCustodian" class="section pt-0 pb-4">
          <h2 class="is-size-3">Data Custodian Tools</h2>
          <div class="column is-three-quarters">
            <div class="card mb-4">
              <div class="card-content">
                <div class="content">
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-clipboard-list" />
                      </span>
                      <span class="tools-link"
                        ><router-link :to="{ name: 'metadata-list' }">Manage Data</router-link>
                      </span>
                    </span>
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-right-left" />
                      </span>
                      <span class="tools-link">
                        <router-link :to="{ name: 'data-access-request-edit' }">Action Data Requests</router-link>
                      </span>
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section pt-0 pb-4">
          <h2 class="is-size-3">Data Requestor Tools</h2>
          <div class="column is-three-quarters">
            <div class="card mb-4">
              <div class="card-content">
                <div class="content">
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-list-check" />
                      </span>
                      <span class="tools-link"
                        ><router-link :to="{ name: 'data-access-request-view' }">Status of Requests</router-link>
                      </span>
                    </span>
                  </p>
                  <p>
                    <span class="icon-text">
                      <span class="icon">
                        <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
                      </span>
                      <span class="tools-link"><router-link :to="{ name: 'search' }">Search</router-link> </span>
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
  <div v-else>
    <PageHeading pageTitle="You are not logged in" />
    <div class="container">
      <div class="section">
        <router-link to="/login" class="mx-auto is-size-5">Log in now</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import PageHeadingWithDescription from '../components/PageHeadingWithDescription.vue';
import PageHeading from '../components/PageHeading.vue';
import { UserGroup } from '@/api/api.types';
import { defineComponent } from 'vue';
import { useUserDataStore } from '@/store';
import type { UserData } from '@/store';

export default defineComponent({
  components: {
    PageHeadingWithDescription,
    PageHeading,
  },
  data(): UserData {
    return useUserDataStore();
  },
  computed: {
    isCustodian() {
      return this.groups?.includes(UserGroup.DataCustodians);
    },
    isAdministrator() {
      return this.groups?.includes(UserGroup.Administrators);
    },
  },
});
</script>

<style scoped>
.tools-link:hover {
  text-decoration: underline;
  color: #073d6e;
}
</style>
