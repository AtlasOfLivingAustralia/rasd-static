<template>
  <o-field :type="type" :label="computedLabel" :variant="computedVariant" :message="computedMessage">
    <div class="is-grid w-full">
      <small v-if="subLabel">{{ subLabel }}</small>
      <slot name="preText" />
      <!-- text, checkbox, select, three-state nullable checkbox, textarea or default slot -->
      <div>
        <o-input
          v-if="['input', 'textarea'].includes(type)"
          :type="type"
          v-model="computedValue"
          @blur="computedIsDirty = true"
          :disabled="disabled"
          :placeholder="placeholder" />
        <o-checkbox
          v-else-if="type === 'checkbox'"
          v-model="computedValue"
          @blur="computedIsDirty = true"
          :disabled="disabled">
          {{ label }}
        </o-checkbox>
        <template v-else-if="type === 'checkbox-boolean'">
          <o-checkbox
            :model-value="computedValue === true"
            @update:modelValue="updateBooleanCheckbox(true, $event)"
            :disabled="disabled">
            Yes
          </o-checkbox>
          <o-checkbox
            :model-value="computedValue === false"
            @update:modelValue="updateBooleanCheckbox(false, $event)"
            :disabled="disabled">
            No
          </o-checkbox>
        </template>
        <div class="is-flex" v-else-if="type === 'datepicker'">
          <o-datepicker v-model="computedValue" @blur="computedIsDirty = true" :disabled="disabled" />
          <o-button v-if="includeReset" @click="this.$emit('reset')">Reset</o-button>
        </div>
        <o-select
          v-else-if="type === 'select'"
          v-model="computedValue"
          @blur="computedIsDirty = true"
          :disabled="disabled">
          <option :value="undefined"></option>
          <option v-for="(option, index) in options" :value="option" :key="index">{{ option }}</option>
        </o-select>
        <slot v-else-if="type === 'shell'" :disabled="disabled" />
        <slot name="postText" />
      </div>
    </div>
  </o-field>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import { Purpose } from '@/api/api.types';
export default defineComponent({
  props: {
    value: {
      type: Object as PropType<string | boolean | undefined>,
      required: false,
    },
    options: {
      type: Object as PropType<string[]>,
      default: () => [] as string[],
    },
    isDirty: {
      type: Object as PropType<boolean | undefined>,
      required: false,
      default: undefined,
    },
    label: { type: String },
    subLabel: { type: String },
    message: { type: String },
    type: {
      type: String,
      default: 'input',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    includeReset: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: '',
    },
  },
  emits: {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:value': function (value: string | boolean | undefined) {
      return true;
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:isDirty': function (value: boolean) {
      return true;
    },
  },
  computed: {
    Purpose() {
      return Purpose;
    },
    computedValue: {
      get() {
        return this.value;
      },
      set(value: string | boolean | undefined) {
        this.$emit('update:value', value);
      },
    },
    computedIsDirty: {
      get(): boolean | undefined {
        // check value for undefined with `isDirty` override
        return this.isDirty || (this.value !== null && typeof this.value !== 'undefined');
      },
      set(isDirty: boolean) {
        this.$emit('update:isDirty', isDirty);
      },
    },
    computedMessage(): string | undefined {
      return this.computedIsDirty && !this.disabled ? this.message : undefined;
    },
    computedVariant(): string | undefined {
      return this.computedIsDirty && !!this.message ? 'danger' : 'success';
    },
    computedLabel(): string | undefined {
      return this.type !== 'checkbox' ? this.label : undefined;
    },
  },
  methods: {
    updateBooleanCheckbox(value: boolean, checked: boolean) {
      const threeStateValue = checked ? value : undefined;
      this.$emit('update:value', threeStateValue);
      this.computedIsDirty = true;
    },
  },
});
</script>
