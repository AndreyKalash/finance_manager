<template>
  <div class="pie_chart">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  chartData: {
    type: Object,
    required: true,
  },
  chartOptions: {
    type: Object,
    default: () => ({}),
  },
  chartType: {
    type: String,
    default: "pie",
  },
});

const canvas = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }
  chartInstance = new Chart(canvas.value.getContext("2d"), {
    type: props.chartType,
    data: props.chartData,
    options: props.chartOptions,
  });
};

onMounted(renderChart);
watch(() => props.chartData, renderChart, { deep: true });
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy();
});
</script>

<style scoped>
.pie_chart {
  width: 300px;
  height: 300px;
  position: relative;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
