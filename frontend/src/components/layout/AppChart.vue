<template>
  <div class="chart">
    <canvas ref="canvas"></canvas>
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
    legend: {
      labels: {
        color: 'white'
      }
    },
    tooltip: {
      callbacks: {
        label: (ctx) =>
          `${ctx.parsed} ${props.unitSymbol || ""} ${ctx.dataset.label || ""}`,
      },
    },
  },
  ...props.chartOptions,
}));

const destroyChart = () => {
  if (chartInstance.value) {
    try {
      chartInstance.value.destroy();
    } catch (error) {
      console.warn("Error destroying chart:", error);
    }
    chartInstance.value = null;
  }
};

const validateCanvas = () => {
  if (!canvas.value) {
    return false;
  }
  
  if (!canvas.value.isConnected) {
    console.warn("Canvas element is not connected to DOM");
    return false;
  }
  
  return true;
};

const initChart = async () => {
    try {
      await nextTick();
      
      if (!validateCanvas()) {
        return;
      }

      const ctx = canvas.value.getContext('2d');
      if (!ctx) {
        console.error("Cannot get 2D context from canvas");
        return;
      }

      destroyChart();

      chartInstance.value = new Chart(ctx, {
        type: props.chartType,
        data: processedData.value,
        options: mergedOptions.value
      });

    } catch (error) {
      console.error("Chart initialization error:", error);
    }
};

onMounted(() => {
  nextTick().then(initChart);
});

watch([processedData, mergedOptions], () => {
  initChart();
}, { deep: true });

watch(() => props.chartType, () => {
  nextTick().then(initChart);
});

onBeforeUnmount(() => {
  destroyChart();
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
