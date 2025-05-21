<template>
  <div class="chart">
    <canvas :key="chartKey" ref="canvas"></canvas>
  </div>
</template>

<script setup>
import {
  ref,
  onMounted,
  watch,
  onBeforeUnmount,
  computed,
  nextTick,
} from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  chartData: { type: Object, required: true },
  chartOptions: { type: Object, default: () => ({}) },
  chartType: {
    type: String,
    default: "pie",
    validator: (value) => ["pie", "bar", "line", "doughnut"].includes(value),
  },
  unitSymbol: { type: String, default: "" },
  sortDesc: { type: Boolean, default: true },
});

const chartKey = ref(0);
const canvas = ref(null);
const chartInstance = ref(null);

const processedData = computed(() => {
  const data = JSON.parse(JSON.stringify(props.chartData));

  if (!props.sort || props.chartType === "line") return data;

  const entries = data.labels
    .map((label, i) => ({
      label,
      data: data.datasets[0].data[i],
      backgroundColor: data.datasets[0].backgroundColor?.[i],
    }))
    .sort((a, b) => b.data - a.data);

  return {
    labels: entries.map((e) => e.label),
    datasets: [
      {
        ...data.datasets[0],
        data: entries.map((e) => e.data),
        backgroundColor: entries.map((e) => e.backgroundColor),
      },
    ],
  };
});

const mergedOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      callbacks: {
        label: (ctx) =>
          `${ctx.parsed} ${props.unit || ""} ${ctx.dataset.label || ""}`,
      },
    },
  },
  ...props.chartOptions,
}));

const initChart = async () => {
  await nextTick();

  if (!canvas.value) {
    console.error("Canvas element not found!");
    return;
  }

  if (chartInstance.value) {
    chartInstance.value.destroy();
    chartInstance.value = null;
  }

  try {
    const ctx = canvas.value.getContext('2d');
    if (!ctx) return;

    chartInstance.value = new Chart(ctx, {
      type: props.chartType,
      data: processedData.value,
      options: mergedOptions.value
    });
  } catch (error) {
    console.error("Chart initialization error:", error);
  }
};

onMounted(initChart);
watch([processedData, mergedOptions], initChart);
watch(() => props.chartType, () => {
  chartKey.value++;
  nextTick().then(initChart);
});
onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
    chartInstance.value = null;
  }
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  position: relative;
  box-sizing: border-box;
}
</style>
