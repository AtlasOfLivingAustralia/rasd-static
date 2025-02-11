<template>
  <PageHeading pageTitle="Create your password" />
  <div class="container">
    <div class="section">
      <o-field label="Username:">
        <o-input
          type="email"
          id="username"
          v-model="username"
          maxlength="200"
          placeholder="Your email address that was used to create this account">
        </o-input>
      </o-field>
      <o-field label="Temporary password:">
        <o-input type="password" id="temp_password" v-model="temp_password" maxlength="50"> </o-input>
      </o-field>

      <o-field label="New password:">
        <o-input
          type="password"
          :class="passwordValidation.passwordClasses"
          @blur="() => validatePassword(this.new_password)"
          v-model="new_password"
          maxlength="50">
        </o-input>
      </o-field>
      <p class="pb-3">
        Your password must be at least 8 characters long and contain at least one lowercase character, one uppercase
        character, one number and one symbol.
      </p>

      <o-field label="Confirm new password:">
        <o-input
          type="password"
          :class="matchValidation.matchClasses"
          @blur="() => validateMatch(this.new_password, this.confirm_password)"
          v-model="confirm_password"
          maxlength="50">
        </o-input>
      </o-field>

      <div class="mt-4 mb-4 container is-flex is-justify-content-space-between is-align-items-center">
        <o-button
          type="submit"
          :class="{ 'is-loading': this.loading }"
          variant="primary"
          :disabled="!isValidated || this.loading"
          @click="createPassword()"
          >Submit</o-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { createPasswordAPI } from '@/api/api';
import { passwordValidator } from '@/helpers/helpers';
import { matchValidator } from '@/helpers/helpers';

export default {
  components: {
    PageHeading,
  },
  data() {
    return {
      username: '',
      temp_password: '',
      new_password: '',
      confirm_password: '',
      passwordValidation: {
        valid: false,
        passwordClasses: '',
      },
      matchValidation: {
        valid: false,
        matchClasses: '',
      },
      loading: false,
    };
  },
  methods: {
    async createPassword() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await createPasswordAPI(this.username, this.temp_password, this.new_password);
      this.loading = false;
      if (this.notification[1] === true) {
        this.$router.push('/login');
        oruga.notification.open({
          variant: 'success',
          message: this.notification,
          position: 'top',
          closable: true,
          duration: 5000,
        });
      } else {
        oruga.notification.open({
          variant: 'danger',
          message: this.notification,
          position: 'top',
          closable: true,
          duration: 10000,
        });
        return this.clearFields();
      }
    },
    clearFields() {
      this.username = '';
      this.new_password = '';
    },
    validatePassword(password) {
      this.passwordValidation = passwordValidator(password);
    },
    validateMatch(field1, field2) {
      this.matchValidation = matchValidator(field1, field2);
    },
  },
  computed: {
    isValidated() {
      return this.username !== '' && this.passwordValidation.valid && this.matchValidation.valid;
    },
  },
};
</script>

<style scoped></style>
