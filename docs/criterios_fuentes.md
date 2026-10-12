# Selección y preparación del corpus

Se incluyen fuentes oficiales relacionadas con el proceso de grado, identificables por URL o por el formato ETIC suministrado por la estudiante. Cada descarga se registra con fecha UTC, tamaño y SHA-256. La fecha de descarga no equivale a fecha de publicación ni garantiza vigencia permanente.

El público objetivo comprende todos los pregrados y modalidades del Politécnico Grancolombiano. El corpus ampliado incorpora reglas generales y 13 apartados de programas virtuales, separados por programa y opción de grado. No constituye cobertura documental exhaustiva. Del Reglamento Estudiantil v8 se seleccionan las páginas 21, 22 y 42, que contextualizan el requisito y la disposición transitoria. La continuidad académica y cohorte pueden modificar la aplicabilidad: el asistente no decide la elegibilidad individual.

La página de entrega que menciona CD-ROM se conserva en inventario y se excluye del índice por actualidad incierta. El reglamento de opciones de grado enlazado desde el portal se excluye temporalmente: es una imagen escaneada y requiere OCR revisado. El enlace de junio de 2024 devolvió HTTP 404; se reemplazó por la versión 8 publicada en 2026. No se incorporan reglas de la Escuela de Negocios, Psicología u otros programas como reglas de Ingeniería de Software.

Se usa extracción PDF con pypdf, HTML con BeautifulSoup y DOCX con python-docx. Los fragmentos se limitan a 180 palabras con 30 de solapamiento, sin unir páginas o secciones diferentes. Se conserva página para PDF y sección para HTML/DOCX; para estos últimos, página 0 significa no aplicable. Una restricción `truncate=false` evita el truncamiento silencioso del embedding.

Los archivos fuente, el corpus textual y la base vectorial se conservan localmente. El repositorio público publica URLs, hashes, código y reportes; no redistribuye los reglamentos o el formato institucional. La preparación de la base no constituye entrenamiento ni fine-tuning de Qwen3.


Actualización de alcance: el público objetivo son todos los pregrados y modalidades del Politécnico Grancolombiano. La cobertura documental específica depende del programa. El corpus distingue programa, modalidad y plantilla; ETIC no es universal. Las evidencias anteriores de semanas 6–9 corresponden al piloto histórico restringido. La nueva ejecución se registra en evidencias/alcance_pregrados. Para consultar un programa puede usarse --programa y --modalidad. La cobertura específica presencial requiere fuentes propias; el chatbot se abstiene ante requisitos no documentados.

