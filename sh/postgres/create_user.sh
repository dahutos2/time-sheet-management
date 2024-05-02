# 「postgres」DBに接続する
psql -d postgres

# postgresユーザーを作成し、パスワードを設定する
CREATE USER postgres WITH PASSWORD 'password';

# postgresユーザーに権限を付与する
ALTER ROLE postgres SUPERUSER CREATEROLE CREATEDB REPLICATION BYPASSRLS;

# ロールの確認
\du

# データベースのオーナーを変更
ALTER DATABASE pj_db OWNER TO postgres;