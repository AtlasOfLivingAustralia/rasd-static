<template>
  <PageHeading pageTitle="Forgot password" />
  <div class="container">
    <div class="section">
      <o-field label="Verification Code">
        <o-input id="code" type="password" v-model="code" maxlength="50"> </o-input>
      </o-field>
      <o-field label="New password">
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

      <o-field label="Confirm new password">
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
          variant="primary"
          :class="{ 'is-loading': this.loading }"
          :disabled="!isValidated || this.loading"
          @click="confirmForgotPassword()"
          >Submit</o-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import PageHeading from '../components/PageHeading.vue';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import { confirmForgotPasswordAPI } from '@/api/api';
import { passwordValidator } from '@/helpers/helpers';
import { matchValidator } from '@/helpers/helpers';

export default {
  components: {
    PageHeading,
  },
  data() {
    return {
      username: '',
      code: '',
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
  mounted() {
    this.username = this.$route.meta.username;
  },
  methods: {
    async confirmForgotPassword() {
      const { oruga } = useProgrammatic();
      this.loading = true;
      this.notification = await confirmForgotPasswordAPI(this.username, this.code, this.new_password);
      this.loading = false;
      oruga.notification.open({
        message: this.notification[0],
        position: 'top',
        closable: true,
        duration: 10000,
        variant: this.notification[1] ? 'success' : 'danger',
      });
      if (this.notification[1]) {
        await this.$router.push('/login');
      } else {
        this.new_pasword = '';
        this.confirm_password = '';
      }
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
      return this.code !== '' && this.passwordValidation.valid && this.matchValidation.valid;
    },
  },
};
</script>

<style scoped></style>
