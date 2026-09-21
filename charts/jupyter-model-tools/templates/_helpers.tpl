{{/* Common labels */}}
{{- define "jupyter-model-tools.labels" -}}
app.kubernetes.io/name: {{ .Release.Name }}-jupyter
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}

{{/* Selector labels */}}
{{- define "jupyter-model-tools.selectorLabels" -}}
app: {{ .Release.Name }}-jupyter
{{- end }}

{{/* Resource name */}}
{{- define "jupyter-model-tools.fullname" -}}
{{ .Release.Name }}-jupyter
{{- end }}

{{/* Secret name: user-provided or chart-generated */}}
{{- define "jupyter-model-tools.secretName" -}}
{{- if .Values.existingSecret -}}
{{ .Values.existingSecret }}
{{- else -}}
{{ include "jupyter-model-tools.fullname" . }}-env
{{- end -}}
{{- end }}
