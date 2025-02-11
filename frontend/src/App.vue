<script setup lang="ts">
import { RouterView } from 'vue-router';
import NavigationBar from '@/components/NavigationBar.vue';
import PageLogos from '@/components/PageLogos.vue';
import PageFooter from '@/components/PageFooter.vue';
import { setAuthHeader, removeAuthHeader } from '@/api/api';
import { useUserDataStore } from '@/store';

// set auth token for the API if any.
const userStore = useUserDataStore();
if (userStore.idToken) {
  setAuthHeader(userStore.idToken);
} else {
  removeAuthHeader();
}
</script>

<template>
  <NavigationBar />
  <RouterView />
  <PageLogos />
  <PageFooter />
</template>
