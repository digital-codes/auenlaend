<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

import { onMounted, ref } from 'vue';

const zoomed = ref(false);

const props = defineProps<{
  text?: string | null;
  src?: string | null;
  audioSrc?: string | null;
  link?: string | null;
  options?: { label: string; title: string }[] | null;
  idx: number;
  last: boolean;
}>();

const emit = defineEmits<{
  (e: 'optionSelected', option: string): void;
  (e: 'indexClicked', idx: number): void;
}>();

const zoom = () => {
  console.log("Zooming image:", props.src);
  zoomed.value = true;
};

const idxClicked = () => {
  console.log("Index clicked:", props.idx);
  emit('indexClicked', props.idx);
}

onMounted(() => {
  console.log("BotResponse mounted with props:", props);
});

</script>

<template>

<va-chip @click="idxClicked">{{ idx }}</va-chip>
  <div class="bot-pane">
    <VaCard>
      <VaCardTitle class="bot-hdr">
        {{ $t("bot.response") }}
      </VaCardTitle>

      <VaCardBlock v-if="text && !src">
          <VaCardContent>
            <span class="bot-text">
              {{ text }}
            </span>
          </VaCardContent>
      </VaCardBlock>

      <VaCardBlock v-if="text && src" horizontal>
        <VaCardBlock class="flex-auto" style="max-width: 60%;">
          <VaCardContent>
            <span class="bot-text">
              {{ text }}
            </span>
          </VaCardContent>
        </VaCardBlock>
        <VaDivider vertical />
        <VaCardBlock class="flex-auto">
          <VaImage v-if="src" class="flex-grow-0 flex-shrink-0 bot-image" :src="src" :ratio="1" fit="scale-down"
            @click="zoom" />
            <p v-if="src.includes('https://upload.wikimedia.org')" class="image-caption">
             © CC-BY 3.0 or 4.0 via Wikimedia Commons
            </p>
        </VaCardBlock>
      </VaCardBlock>

      <VaCardBlock v-if="!text && src" horizontal>
        <VaCardBlock class="flex-auto" style="max-width: 60%;">
          <VaCardContent>
            <span class="bot-text">
              {{ $t("bot.onlyImage") }}
            </span>
          </VaCardContent>
        </VaCardBlock>
        <VaDivider vertical />
        <VaCardBlock class="flex-auto">
          <VaImage v-if="src" class="flex-grow-0 flex-shrink-0 bot-image" :src="src" :ratio="1" fit="scale-down"
            @click="zoom" />
            <p v-if="src.includes('https://upload.wikimedia.org')" class="image-caption">
             © CC-BY 3.0 or 4.0 via Wikimedia Commons
            </p>
        </VaCardBlock>
      </VaCardBlock>

      <VaCard v-if="link" :href="link" target="_blank">
        <VaCardTitle>
          Link
        </VaCardTitle>
        <VaCardContent class="bot-link">
          {{ link }}
          <VaIcon name="open_in_new" class="ml-1" size="1.5rem" :color='"var(--va-info)"' :alt="t('openNew')" />
        </VaCardContent>
      </VaCard>
      <VaCard v-if="audioSrc">
        <VaCardTitle>
          © Frommolt, Karl-Heinz , Tierstimmenarchiv - Museum für Naturkunde Berlin CC-BY-SA-NC 4.0
        </VaCardTitle>
        <VaCardContent class="audio">
          <audio :src="audioSrc" controls autoplay class="bot-audio" />
        </VaCardContent>
      </VaCard>
      <VaCard v-if="options && options.length > 0">
        <VaCardTitle>
          {{$t("bot.options")}}
        </VaCardTitle>
        <VaCardContent>
          <div class="options-pane mt-4">
            <va-button v-for="(option, idx) in options" :key="idx" class="m-2 mr-2" color="primary"
              @click="emit('optionSelected', option.title)" :disabled="!last">
              {{ option.label }}
            </va-button>
          </div>
        </VaCardContent>
      </VaCard>
    </VaCard>
  </div>


  <VaModal v-if="src" v-model="zoomed" fullscreen hide-default-actions :close-button="true">
    <div class="flex flex-col gap-2">
      <p v-if="text" class="text-center text-sm text-gray-500 mt-2 bot-modal-text">
        {{ text }}
      </p>
      <VaImage :src="props.src || ''" fit="contain" :ratio="1" class="bot-modal-image" />
    </div>
  </VaModal>

</template>

<style scoped>
.bot-pane {
  padding: 4px;
  border-radius: 8px;
  height: 100%;
  width: 90%;
  box-sizing: border-box;
  color: var(--va-info);
  background-color: var(--va-background-primary);
  /*, #f8d7da);*/
  margin-right: 1rem;
}

.bot-text {
  color: var(--va-info);
}

.bot-hdr {
  font-size: 120%;
  font-weight:400;
}

.bot-link {
  color: var(--va-primary);
  text-decoration: underline;
  cursor: pointer;
}

.bot-audio {
  max-width: 50%;
}

.bot-image {
  /*
    border: solid 3px red;
    */
  min-width: 30%;
  max-width: 300px;
  cursor: pointer;
  min-height: 100px;
  max-height: 200px;
  box-sizing: border-box;
  padding: .5rem;
  margin-left:auto;
  margin-right:auto;
}

.bot-modal-image {
  max-height: 80vh;
  box-sizing: border-box;
  padding: .5rem;
}

.bot-modal-text {
  color: var(--va-info);
  text-align: center;
  max-height: 15vh;
  overflow-y: scroll;
  box-sizing: border-box;
  padding: .5rem;
  margin: .5rem;
  margin-right: 3rem;
  /* close button space */
}

/*
img {
  display: block;
  margin-top: 12px;
  max-width: 100%;
  min-width: 30%;
  height: auto;
  max-height: 50%;
  margin-left: auto;
  margin-right: auto;
}
*/
label {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}
</style>

<style scoped lang="scss">
@use "sass:color";
@use '@/style/colors.scss';

.va-card {
  background-color: light-dark(colors.$dash-bg2-light, colors.$dash-bg2-dark);
}
</style>

<style>
.va-modal__close {
  color: var(--va-danger);
  background-color: var(--va-background-primary);
}
</style>