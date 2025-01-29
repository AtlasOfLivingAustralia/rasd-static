<template>
  <div class="hero-image" alt="A background image of a native australian plant">
    <div class="filter"></div>
    <div class="container">
      <div class="rows is-flex is-flex-direction-column">
        <div class="row is-one-half">
          <h1 class="title is-1 has-text-centered has-text-white" id="title">Restricted Access Species Data Service</h1>
          <p class="subtitle is-3 has-text-centered has-text-white pt-1">
            Facilitating discovery and requests for restricted access species data
          </p>
        </div>
        <div class="column box has-background-primary pt-5 pb-0" id="hero-description">
          <h1 class="subtitle is-3 row has-text-white ml-2">What is Restricted Access Species Data?</h1>
          <div class="is-flex is-flex-wrap-wrap is-flex-direction-row is-justify-content-space-between">
            <p class="column subtitle has-text-white child-div mr-4 pr-4 pt-0">
              Restricted access species data are biodiversity datasets that contain information that may compromise
              people, species, personal property or landholdings and that have some restriction over the availability of
              the data.
              <span class="is-inline-block pt-5">
                For more information about the framework see the
                <a :href="rasd_UI_framework_url" class="has-text-white is-underlined"
                  >Restricted Access Species Data Framework.</a
                ></span
              >
              <span class="is-inline-block pt-4">
                For more information about the data service see the
                <router-link to="about" class="has-text-white is-underlined">About page.</router-link></span
              >
            </p>

            <div class="column is-flex-grow-0 mx-auto mb-auto pr-6">
              <router-link to="search">
                <button class="button is-secondary is-large px-6 py-6 is-hoverable">
                  Search
                  <font-awesome-icon class="pl-3" icon="fa-solid fa-magnifying-glass" />
                </button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import testingJson from './../../testing.json';
import productionJson from './../../production.json';

let config = testingJson;

const defaultConfig = {
  rasd_UI_framework_url: 'https://rasd.org.au',
  termsOfUseUrl: 'https://service.rasd.org.au/#/terms-of-use',
  privacyPolicyUrl: 'https://service.rasd.org.au/#/privacy-notice',
};

export default {
  created() {
    const currentDomain = window.location.hostname;
    // Determine the appropriate JSON file based on the domain
    if (currentDomain === 'service.testing.rasd.org.au' || currentDomain === 'localhost') {
      this.jsonData = testingJson;
    } else if (currentDomain === 'service.rasd.org.au') {
      this.jsonData = productionJson;
    } else {
      console.warn('Unknown domain:', currentDomain);
      const frameworkUrl = currentDomain.includes('service.') ? currentDomain.replace('service.', '') : 'rasd.org.au';
      this.jsonData = {
        rasd_UI_framework_url: `https://${frameworkUrl}`,
        termsOfUseUrl: `https://${currentDomain}/#/terms-of-use`,
        privacyPolicyUrl: `https://${currentDomain}/#/privacy-notice`,
      };
    }
    // Access the JSON data
    if (this.jsonData) {
      console.log('JSON Data:', this.jsonData);
    } else {
      console.warn('No JSON data found');
      this.jsonData = defaultConfig;
    }
    console.log('rasd_UI_framework_url:', this.jsonData.rasd_UI_framework_url);
    if (null != config && config !== this.jsonData) {
      config = this.jsonData;
    }
  },
  data() {
    return {
      rasd_UI_framework_url: config.rasd_UI_framework_url || 'https://rasd.org.au',
    };
  },
};
</script>

<style scoped>
#hero-description {
  margin-top: 30vh;
}

#title {
  padding-top: 12rem;
  font-size: 3rem;
}

.hero-image {
  background-image: url('../assets/hero_image.jpeg');
  position: relative;
  height: auto;
  min-height: 100vh;
  background-size: cover;
  background-position: center center;
  margin-bottom: -20rem;
}

.filter {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  opacity: 0.8;
  background: linear-gradient(0deg, transparent 10%, #073d6e 100%);
}
</style>
