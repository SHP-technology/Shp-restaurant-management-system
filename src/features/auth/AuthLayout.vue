<template>
  <main class="auth-page">
    <section class="auth-visual" aria-label="Restaurant dining room">
      <div class="auth-visual-content">
        <RouterLink to="/" class="inline-flex items-center gap-2 text-xs font-bold text-white/90 hover:text-[#f47b20] transition mb-6">
          <ArrowLeft :size="14" /> Back to Home
        </RouterLink>
        <p class="auth-brand">SHP <span>/</span> RESTAURANT OS</p>
        <h1>Good food.<br /><em>Great moments.</em></h1>
        <p class="auth-visual-copy">{{ description }}</p>
      </div>
      <p class="auth-visual-caption">Thoughtfully built for the people behind the pass.</p>
    </section>
    <section class="auth-form-panel">
      <div class="auth-form-wrap">
        <p class="auth-eyebrow">{{ eyebrow }}</p>
        <h2>{{ title }}</h2>
        <p class="auth-description">{{ description }}</p>
        <slot />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'

defineProps<{
  eyebrow: string
  title: string
  description: string
}>()
</script>
