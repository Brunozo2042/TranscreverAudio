from pathlib import Path            # Utilizado para administrar diretórios
import speech_recognition as sr     # Utilizado para a transcrição
from pydub import AudioSegment      # Utilizado para a conversão de mp3 -> wav

# DEPENDÊNCIAS  
# pydub - pip install pydub
# SpeechRecognition - pip install SpeechRecognition

# Diretórios
dir_audio = Path("./audios")
dir_txt = Path("./txt")

# Cria a pasta de saída se não existir
dir_txt.mkdir(exist_ok=True)

# Inicializa o reconhecedor
reconhecedor = sr.Recognizer()

# Tamanho do segmento em segundos
DURACAO_SEGMENTO = 30

# Itera sobre todos os arquivos na pasta
for arquivo in dir_audio.iterdir():
    if arquivo.is_file() and arquivo.suffix in [".wav", ".mp3", ".flac"]:  # Verifica se é um arquivo de áudio
        try:
            arquivo_wav = None  # Variável para armazenar o arquivo WAV convertido
            
            # Converte MP3 ou outros formatos para WAV se necessário
            if arquivo.suffix != ".wav":
                arquivo_wav = dir_audio / f"{arquivo.stem}.wav"
                AudioSegment.from_file(str(arquivo)).export(arquivo_wav, format="wav")
                arquivo = arquivo_wav

            # Cria o arquivo de texto correspondente
            nome_txt = dir_txt / f"{arquivo.stem}.txt"
            with nome_txt.open("w", encoding="utf-8") as f:
                print(f"Iniciando transcrição de: {arquivo.name}")

                # Carrega o áudio
                with sr.AudioFile(str(arquivo)) as fonte_audio:
                    duracao_total = int(fonte_audio.DURATION)  # Duração total do áudio
                    offset = 0  # Início do segmento

                    while offset < duracao_total:
                        # Processa um segmento de áudio de DURACAO_SEGMENTO segundos
                        print(f"Transcrevendo segmento {offset} - {offset + DURACAO_SEGMENTO}s...")
                        audio_segment = reconhecedor.record(
                            fonte_audio,
                            offset=offset,
                            duration=DURACAO_SEGMENTO
                        )

                        # Tenta reconhecer o texto no segmento
                        try:
                            texto_segmento = reconhecedor.recognize_google(audio_segment, language="pt")
                            f.write(texto_segmento + "\n")  # Salva o texto parcial no arquivo
                        except sr.UnknownValueError: 
                            print(f"Segmento {offset}-{offset + DURACAO_SEGMENTO}s: Não foi possível reconhecer o áudio.")
                            f.write("[Inaudível]\n")
                        except sr.RequestError as e:
                            print(f"Erro na API do Google: {e}")
                            f.write("[Erro na API]\n")

                        # Avança para o próximo segmento
                        offset += DURACAO_SEGMENTO

            # Deleta o arquivo .wav se foi criado anteriormente
            if arquivo_wav and arquivo_wav.exists():
                arquivo_wav.unlink()
            
            print(f"Transcrição concluída: {nome_txt}")
        
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
