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
                <a href="https://rasd.org.au/" class="has-text-white is-underlined"
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
                  <font-awesome-icon icon="fa-solid fa-magnifying-glass" class="pl-3" />
                </button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

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
