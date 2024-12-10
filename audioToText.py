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

            # Converte o caminho para string antes de usar sr.AudioFile
            with sr.AudioFile(str(arquivo)) as fonte_audio:
                audio = reconhecedor.record(fonte_audio)  # Carrega o áudio
                
            # Reconhece o texto usando o serviço padrão (Google Web Speech API)
            texto = reconhecedor.recognize_google(audio, language="pt")
            
            # Cria o arquivo de texto correspondente
            nome_txt = dir_txt / f"{arquivo.stem}.txt"
            with nome_txt.open("w", encoding="utf-8") as f:
                f.write(texto)

            # Deleta o arquivo .wav se foi criado anteriormente
            if arquivo_wav and arquivo_wav.exists():
                arquivo_wav.unlink()
            
            print(f"Transcrição salva: {nome_txt}")
        
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
