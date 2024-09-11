# Define o nome da tarefa
$taskName = "EZBoot"

# Define o caminho completo para o executável do programa que você quer iniciar
$programPath = "C:\Program Files (x86)\EZBoot\EZBoot.exe"

# Define a descrição da tarefa
$taskDescription = "Inicia o meu programa automaticamente quando o Windows inicia"

# Cria a ação para iniciar o programa
$action = New-ScheduledTaskAction -Execute $programPath

# Cria o gatilho para iniciar a tarefa no logon do usuário
$trigger = New-ScheduledTaskTrigger -AtLogOn 

# Define configurações adicionais para a tarefa
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RunOnlyIfNetworkAvailable

# Define o principal da tarefa para executar com privilégios elevados
$principal = New-ScheduledTaskPrincipal -UserId (whoami) -LogonType Interactive -RunLevel Highest

# Registra a tarefa no Agendador de Tarefas
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Description $taskDescription -Settings $settings

Write-Output "Tarefa '$taskName' criada com sucesso para iniciar '$programPath' ao logar no Windows com privilégios máximos."
