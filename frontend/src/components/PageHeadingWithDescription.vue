<template>
  <div class="heading-image" alt="a header image of a Dicksonia Antarctica fern">
    <div class="filter"></div>
    <div class="container pt-6">
      <div class="section">
        <h1 class="title has-text-white is-1 mt-5 pt-6">{{ pageTitle }}</h1>
        <span class="subtitle has-text-white is-inline">
          <p class="is-inline pr-5">{{ pageDescription }}</p>
          <p class="is-inline pl-6">{{ extraDescription }}</p>
        </span>
      </div>
    </div>
    2
  </div>
</template>

<script>
export default {
  name: 'PageHeadingWithDescription',
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
    pageDescription: {
      type: String,
      required: true,
    },
    extraDescription: {
      type: String,
      required: false,
    },
  },
};
</script>

<style scoped>
.heading-image {
  background-image: url('../assets/heading_image.jpeg');
  position: relative;
  height: auto;
  min-height: 22rem;
  background-size: cover;
  background-position: center center;
}

.filter {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  opacity: 0.85;
  background: linear-gradient(0deg, transparent 0, #142b3e 70%), linear-gradient(90deg, #142c3f 70%, transparent 120%);
}
</style>
