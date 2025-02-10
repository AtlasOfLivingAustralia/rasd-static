<template>
  <button class="green">
    {{ label }}
  </button>
</template>

<script>
export default {
  name: 'CustomButton',
  props: {
    label: {
      type: String,
      default: '',
    },
  },
};
</script>

<style scoped></style>
