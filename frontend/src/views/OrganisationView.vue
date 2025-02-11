<template>
  <PageHeading pageTitle="Organisation / Edit" />
  <div class="container">
    <div v-if="organisation" class="section">
      <router-link to="/organisations">Go back to Organisations List</router-link>
      <o-notification v-if="notificationContent" closable aria-close-label="Close notification"
        >{{ notificationContent }}
      </o-notification>
      <div class="field pt-4">
        <o-field class="label">Entity Name:</o-field>
        <o-input
          v-model="organisation.name"
          :class="this.nameValidation.nameClasses"
          maxlength="200"
          @blur="() => validateName(this.organisation.name)"
          disabled></o-input>
      </div>
      <div class="label">
        <o-field class="is-half">ABN:</o-field>
        <o-input
          v-model="organisation.abn"
          :class="this.abnValidation.abnClasses"
          @blur="() => validateABN(this.organisation.abn)"
          disabled></o-input>
      </div>
      <div class="label">
        <o-field class="is-half">Email:</o-field>
        <o-input
          v-model="organisation.email"
          :class="this.emailValidation.emailClasses"
          @blur="() => validateEmail(this.organisation.email)"
          :disabled="!editMode"></o-input>
      </div>
      <div class="is-flex is-justify-content-start pt-6">
        <o-button class="button" variant="primary" @click="this.setEditMode()">{{
          editMode ? 'Cancel' : 'Edit'
        }}</o-button>
        <o-button
          v-if="this.editMode"
          class="button is-success mr-4"
          :class="{ 'is-loading': this.loading }"
          :disabled="this.loading"
          @click="this.editOrganisation()"
          >Save</o-button
        >
      </div>
    </div>
    <div v-else class="section">
      <o-loading />
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import { editOrganisationAPI, getOrganisationAPI } from '../api/api';
import { abnValidator, emailValidator, nameValidator } from '@/helpers/helpers';
import { useProgrammatic } from '@oruga-ui/oruga-next';

export default {
  name: 'OrganisationView',
  components: {
    PageHeading,
  },
  data() {
    return {
      loading: false,
      organisation: null,
      organisationViewData: null,
      editMode: false,
      nameValidation: {
        valid: false,
        nameClasses: '',
      },
      abnValidation: {
        valid: false,
        abnClasses: '',
      },
      emailValidation: {
        valid: false,
        emailClasses: '',
      },
      notificationContent: null,
    };
  },
  beforeMount() {
    this.getOrganisation();
  },
  watch: {
    organisation() {
      this.loading = false;
    },
  },
  methods: {
    async getOrganisation() {
      this.loading = true;
      this.organisation = await getOrganisationAPI(this.$route.params.id);
      this.organisationViewData = JSON.parse(JSON.stringify(this.organisation));
    },
    setEditMode() {
      this.editMode = !this.editMode;
      if (!this.editMode) {
        this.organisation.email = JSON.parse(JSON.stringify(this.organisationViewData.email));
      }
    },
    async editOrganisation() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await editOrganisationAPI(this.organisation.id, this.organisation.email);
      this.loading = false;
      if (this.notification) {
        oruga.notification.open({
          message: this.notification[0],
          position: 'top',
          variant: this.notification[1] ? 'success' : 'danger',
          closable: true,
        });
      }
      if (this.notification[1]) {
        this.editMode = false;
        setTimeout(() => {
          this.$router.go(0);
        }, 3000);
      }
    },
    validateName(name) {
      this.nameValidation = nameValidator(name);
    },
    validateABN(abn) {
      this.abnValidation = abnValidator(abn);
    },
    validateEmail(email) {
      this.emailValidation = emailValidator(email);
    },
  },
};
</script>

<style scoped></style>
