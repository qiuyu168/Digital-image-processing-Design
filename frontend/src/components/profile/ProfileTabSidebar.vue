<template>
  <aside class="tab-sidebar">
    <span class="eyebrow">Settings</span>
    <div class="tab-list">
      <div
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-item"
        :class="{ active: activeTab === tab.key }"
        @click="$emit('update:activeTab', tab.key)"
      >
        {{ tab.label }}
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  activeTab: { type: String, required: true },
  tabs: { type: Array, required: true }
})

defineEmits(['update:activeTab'])
</script>

<style scoped>
.tab-sidebar {
  position: sticky;
  top: 96px;
  align-self: flex-start;
  padding: 4px 0;
}

.eyebrow {
  display: block;
  padding: 0 14px 12px;
  font-size: 11px;
  font-weight: 700;
  color: var(--c-amber);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.tab-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-left: 1px solid var(--c-line);
}

.tab-item {
  position: relative;
  padding: 10px 16px;
  color: var(--c-ink-2);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color var(--dur-fast) var(--ease-standard), background var(--dur-fast) var(--ease-standard);

  &::before {
    content: "";
    position: absolute;
    left: -1px;
    top: 8px;
    bottom: 8px;
    width: 2px;
    border-radius: 2px;
    background: var(--c-amber);
    opacity: 0;
    transition: opacity var(--dur-fast) var(--ease-standard);
  }

  &:hover {
    color: var(--c-ink);
  }

  &.active {
    color: var(--c-ink);
    font-weight: 600;
    background: var(--c-cream-2);

    &::before {
      opacity: 1;
    }
  }
}

@media (max-width: 900px) {
  .tab-sidebar {
    position: relative;
    top: 0;
  }

  .eyebrow {
    padding: 0 0 12px;
  }

  .tab-list {
    flex-direction: row;
    flex-wrap: wrap;
    border-left: none;
    border-bottom: 1px solid var(--c-line);
    gap: 0;
  }

  .tab-item {
    padding: 10px 16px;

    &::before {
      left: 8px;
      right: 8px;
      top: auto;
      bottom: -1px;
      width: auto;
      height: 2px;
    }
  }
}
</style>
