<template>
  <div class="pie_chart">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount, computed } from "vue";
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
  unitSymbol: {
    type: String,
    default: ""
  },
  sortDesc: {
    type: Boolean,
    default: true
  }
});

const canvas = ref(null);
let chartInstance = null;

const sortedChartData = computed(() => {
  if (!props.sortDesc) return props.chartData;

  const data = JSON.parse(JSON.stringify(props.chartData));
  const labels = data.labels || [];
  const datasets = data.datasets || [{}];

  const entries = labels.map((label, index) => ({
    label,
    data: datasets[0].data?.[index] || 0,
    color: datasets[0].backgroundColor?.[index] || "#000000"
  }));

  entries.sort((a, b) => b.data - a.data);

  return {
    labels: entries.map(e => e.label),
    datasets: [{
      ...datasets[0],
      data: entries.map(e => e.data),
      backgroundColor: entries.map(e => e.color)
    }]
  };
});

const mergedOptions = computed(() => ({
  ...props.chartOptions,
  plugins: {
    ...props.chartOptions.plugins,
    tooltip: {
      ...props.chartOptions.plugins?.tooltip,
      callbacks: {
        label: (context) => {
          const value = context.parsed || 0;
          const defaultLabel = context.dataset.label || '';
          return `${value}${props.unitSymbol ? ' ' + props.unitSymbol : ''} ${defaultLabel}`;
        }
      }
    }
  }
}));

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(canvas.value.getContext("2d"), {
    type: props.chartType,
    data: sortedChartData.value,
    options: mergedOptions.value
  });
};

onMounted(renderChart);
watch([() => sortedChartData.value, () => mergedOptions.value], renderChart);
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
