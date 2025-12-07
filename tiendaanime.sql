-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-06-2025 a las 06:36:52
-- Versión del servidor: 11.5.2-MariaDB
-- Versión de PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tiendaanime`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'clientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Producto', 7, 'add_producto'),
(26, 'Can change Producto', 7, 'change_producto'),
(27, 'Can delete Producto', 7, 'delete_producto'),
(28, 'Can view Producto', 7, 'view_producto'),
(29, 'Can add Categoría', 8, 'add_categoria'),
(30, 'Can change Categoría', 8, 'change_categoria'),
(31, 'Can delete Categoría', 8, 'delete_categoria'),
(32, 'Can view Categoría', 8, 'view_categoria'),
(33, 'Can add carrito', 9, 'add_carrito'),
(34, 'Can change carrito', 9, 'change_carrito'),
(35, 'Can delete carrito', 9, 'delete_carrito'),
(36, 'Can view carrito', 9, 'view_carrito');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$W2Gr9eG1XtaerL5qA4MDtk$c5PxSYXj9KCHLE6zGFemEuLTWL0PWH3dHSyIknWYqQE=', '2025-06-13 04:35:04.142312', 1, 'Juanito', '', '', '', 1, 1, '2025-06-12 07:04:34.600791'),
(2, 'pbkdf2_sha256$1000000$ZMXvfC0lLgzycJxpbqSwok$kgAe2v15JMPhMnPPTsNB36AHlW2JKVE7qJEkE43Ko/E=', '2025-06-13 02:48:45.586095', 0, 'jon', '', '', '', 0, 1, '2025-06-13 01:56:24.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-06-12 07:05:30.998167', '1', 'Figuras de anime', 1, '[{\"added\": {}}]', 8, 1),
(2, '2025-06-12 07:05:39.326477', '2', 'Cartas', 1, '[{\"added\": {}}]', 8, 1),
(3, '2025-06-12 07:05:46.387653', '3', 'Dulces', 1, '[{\"added\": {}}]', 8, 1),
(4, '2025-06-12 07:06:02.984993', '4', 'Peluches', 1, '[{\"added\": {}}]', 8, 1),
(5, '2025-06-12 07:06:10.693327', '5', 'Juegos de mesa', 1, '[{\"added\": {}}]', 8, 1),
(6, '2025-06-12 07:06:16.820438', '6', 'Posters', 1, '[{\"added\": {}}]', 8, 1),
(7, '2025-06-12 07:06:23.691998', '7', 'Llaveros', 1, '[{\"added\": {}}]', 8, 1),
(8, '2025-06-12 07:06:29.246005', '8', 'Papelería', 1, '[{\"added\": {}}]', 8, 1),
(9, '2025-06-12 07:06:40.213948', '9', 'Puzzles', 1, '[{\"added\": {}}]', 8, 1),
(10, '2025-06-12 07:06:56.633139', '10', 'Prendas', 1, '[{\"added\": {}}]', 8, 1),
(11, '2025-06-12 07:07:04.676060', '11', 'Bebidas', 1, '[{\"added\": {}}]', 8, 1),
(12, '2025-06-12 22:22:55.732859', '12', 'Ramen', 1, '[{\"added\": {}}]', 8, 1),
(13, '2025-06-13 01:56:24.815403', '2', 'jon', 1, '[{\"added\": {}}]', 4, 1),
(14, '2025-06-13 01:56:33.642201', '2', 'jon', 2, '[{\"changed\": {\"fields\": [\"Active\"]}}]', 4, 1),
(15, '2025-06-13 01:57:33.268737', '2', 'jon', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(16, '2025-06-13 01:57:42.994510', '2', 'jon', 2, '[{\"changed\": {\"fields\": [\"Active\"]}}]', 4, 1),
(17, '2025-06-13 03:32:50.690205', '1', 'clientes', 1, '[{\"added\": {}}]', 3, 1),
(18, '2025-06-13 04:31:06.510476', '4', 'Kriss', 3, '', 4, 1),
(19, '2025-06-13 04:31:21.899029', '6', 'Jooon', 3, '', 4, 1),
(20, '2025-06-13 04:32:26.080022', '5', 'Joon', 3, '', 4, 1),
(21, '2025-06-13 04:32:31.277778', '3', 'Kris', 3, '', 4, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(9, 'sysApp', 'carrito'),
(8, 'sysApp', 'categoria'),
(7, 'sysApp', 'producto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-12 07:03:18.135591'),
(2, 'auth', '0001_initial', '2025-06-12 07:03:18.590024'),
(3, 'admin', '0001_initial', '2025-06-12 07:03:18.698276'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-12 07:03:18.705370'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-12 07:03:18.714374'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-12 07:03:18.777469'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-12 07:03:18.823635'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-06-12 07:03:18.850159'),
(9, 'auth', '0004_alter_user_username_opts', '2025-06-12 07:03:18.856334'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-06-12 07:03:18.891224'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-06-12 07:03:18.893228'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-12 07:03:18.902912'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-06-12 07:03:18.926596'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-12 07:03:18.951601'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-06-12 07:03:18.973296'),
(16, 'auth', '0011_update_proxy_permissions', '2025-06-12 07:03:18.986401'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-12 07:03:19.009954'),
(18, 'sessions', '0001_initial', '2025-06-12 07:03:19.044957'),
(19, 'sysApp', '0001_initial', '2025-06-12 07:03:19.057012'),
(20, 'sysApp', '0002_categoria_alter_producto_options_producto_stock_and_more', '2025-06-12 07:03:19.129943'),
(21, 'sysApp', '0003_carrito', '2025-06-12 07:03:19.173606'),
(22, 'sysApp', '0004_producto_descripcion', '2025-06-12 07:03:19.194985'),
(23, 'sysApp', '0005_alter_producto_precio', '2025-06-12 07:03:19.227512');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('4ou729eczk9d67r62lq92ol6kj6ib4nj', '.eJyNzt1Kw0AQBeBXGeY6Nk2skuRulVhMS1Oa5sYfZN0MdTXJhs2ugqXv7lKLRBTr7TnDmW-LgmstjcLkdouywuTUQyONrV2CS6qteCJYqhdqVAvRHcKVJaGEgoy_v3FNPXrYaRLS3YeTOB6Pxp7bbI2suFs797C3j0YZXmMSuH6yP5AN31DrPvgNVZL7nVaVFUb1_r4ZPXe0wZ33KTr7QxSEkNIr0a-c-AcnGHK--iOah_C7J4yGoHyerhgUbJ2vSpjmWQ6H6GLOFpcMTiArs3JdlDBj10W6cME0TWc3A2hwBBr8GxodpPe7D0V1lG4:1uPtXp:YeejEi2i1PNGpUeiFtzlZodsl5Xy9Q4HedC9JnlX0Yc', '2025-06-13 02:19:25.224040'),
('bw3fd2nm6ql9pqidn38r3matn8kicje2', '.eJxNzLEKgzAUheFXCXcOUeukm0OrUtBi6lBKKakJcosaiddJfPemnbqe__Bt0CnnkCyk9w1QQxrFHAhpHfwEUhTiVOZt1lwlk-3l2DCZlbesYrKuWF6fW-AwO9Ohf8dRkoQi5J6cCLX6YhyW9UWW1PDXcVS9mTwfjEajCmZn9dqRXYJfeUYH8Z5ND_tj_wAHtTE2:1uPtMJ:Wbs9IFtXadGTlhJRQyx9UddlytB09sRkNjDTw9yshUo', '2025-06-13 02:07:31.663220'),
('fvih5z6krxpoo0ws1on7kep534qtwszr', '.eJxVjM0OwiAQhN-FsyEIXX48evcZyC5spWogKe3J-O62SQ-auc33zbxFxHUpce08xymLi9Di9NsRpifXHeQH1nuTqdVlnkjuijxol7eW-XU93L-Dgr1s69GroEZt0Q_BkzUpOLXF-bOz2gA5g0oR5ASg2bD1CMAmEw3ZIkMSny-0BDdN:1uPuRF:dtcblhJZQ13L_KoY3V_fcPgy2H3WaWu4ExJkYlIBFqw', '2025-06-13 03:16:41.140525'),
('ol0li8w9fj4rxyzr1b73w8iiyddc3uew', '.eJxVjEEOwiAQRe_C2hBgCi0u3XsGMswMtmpoUtqV8e7apAvd_vfef6mE2zqmrcmSJlZnZdXpd8tID6k74DvW26xprusyZb0r-qBNX2eW5-Vw_w5GbOO3HtgjZUs-WyjRWecGB5LB-GAkxK6j0gWQ2JuevAWkGIApo_QMhY1X7w_WGTfH:1uPc2w:AbeabLlaTfnpeGfYR0LI0vaKVYpB8IADkeh6QRx8pU0', '2025-06-12 07:38:22.478261'),
('qgh03p81kxcxp3s3a5ijlpsler8na9gs', '.eJxVjEEOwiAQRe_C2hBgCi0u3XsGMswMtmpoUtqV8e7apAvd_vfef6mE2zqmrcmSJlZnZdXpd8tID6k74DvW26xprusyZb0r-qBNX2eW5-Vw_w5GbOO3HtgjZUs-WyjRWecGB5LB-GAkxK6j0gWQ2JuevAWkGIApo_QMhY1X7w_WGTfH:1uPtBJ:1EfQekm657hpoR_rd3fDXfnGLhlsafB9sLu2_YBWOtQ', '2025-06-13 01:56:09.564933'),
('r5ya2dolw1k2gsdrdxu4l5809f1tesmx', '.eJxVjEEOwiAQRe_C2hBgCi0u3XsGMswMtmpoUtqV8e7apAvd_vfef6mE2zqmrcmSJlZnZdXpd8tID6k74DvW26xprusyZb0r-qBNX2eW5-Vw_w5GbOO3HtgjZUs-WyjRWecGB5LB-GAkxK6j0gWQ2JuevAWkGIApo_QMhY1X7w_WGTfH:1uPr9M:bDe9KWfSMl0-48ByHBlu3FZ3v9eZ3aWCRymyu9mk-JI', '2025-06-12 23:46:00.539273'),
('vxi4sgjwwixq79v0hdamh3cdvjz7qa17', '.eJxVjEEOwiAQRe_C2hBgCi0u3XsGMswMtmpoUtqV8e7apAvd_vfef6mE2zqmrcmSJlZnZdXpd8tID6k74DvW26xprusyZb0r-qBNX2eW5-Vw_w5GbOO3HtgjZUs-WyjRWecGB5LB-GAkxK6j0gWQ2JuevAWkGIApo_QMhY1X7w_WGTfH:1uPvb2:AXhmz0ZhqMkZTk30lXadELRQdOa1YPEWVmBH1NPbY8U', '2025-06-13 04:30:52.778593'),
('z4skwi7sto08orke1bhdqlyr5gkoew2b', '.eJxVjM0OwiAQhN-FsyEIXX48evcZyC5spWogKe3J-O62SQ-auc33zbxFxHUpce08xymLi9Di9NsRpifXHeQH1nuTqdVlnkjuijxol7eW-XU93L-Dgr1s69GroEZt0Q_BkzUpOLXF-bOz2gA5g0oR5ASg2bD1CMAmEw3ZIkMSny-0BDdN:1uPuTM:vVTklCkv5vkNvj-o0qlLmOCdaHevPjXdIZ6A7KD46yo', '2025-06-13 03:18:52.982526');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sysapp_carrito`
--

CREATE TABLE `sysapp_carrito` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sysapp_categoria`
--

CREATE TABLE `sysapp_categoria` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sysapp_categoria`
--

INSERT INTO `sysapp_categoria` (`id`, `nombre`, `descripcion`, `fecha_creacion`) VALUES
(1, 'Figuras de anime', 'Las figuras de anime son representaciones físicas de personajes de anime y manga. Pueden ser estáticas, detalladas y hechas de materiales como PVC o resina. Son populares entre coleccionistas y fanáticos del anime, y varían en tamaño, desde pequeñas figuras de 10-15 cm hasta versiones más grandes. Están disponibles en diferentes estilos, basadas en escenas o poses características de los personajes.', '2025-06-12 07:05:30.997164'),
(2, 'Cartas', 'Las cartas son tarjetas coleccionables que presentan ilustraciones de personajes, escenas o temas de series de anime. A menudo, se utilizan en juegos de cartas coleccionables, donde los jugadores compiten usando cartas con habilidades o poderes. También pueden ser simplemente objetos de colección, con imágenes de alta calidad. Las cartas de anime suelen ser populares entre los fanáticos, y algunas ediciones especiales o limitadas pueden tener un gran valor entre los coleccionistas.', '2025-06-12 07:05:39.325264'),
(3, 'Dulces', 'Los dulces japoneses son una variedad de golosinas tradicionales y modernas originarias de Japón. Incluyen una amplia gama de sabores, texturas y presentaciones, desde galletas y caramelos hasta chocolates y gomitas. Muchos dulces japoneses tienen sabores únicos como té verde, frambuesa, matcha o red bean (frijol rojo). También son conocidos por su aspecto creativo y colorido. Los dulces japoneses se disfrutan tanto en Japón como internacionalmente, y algunos se venden en cajas temáticas o en versiones limitadas.', '2025-06-12 07:05:46.387653'),
(4, 'Peluches', 'Los peluches son muñecos suaves y rellenos, generalmente hechos de materiales como felpa o algodón. A menudo representan animales, personajes de anime, o figuras de fantasía, y son populares tanto entre niños como adultos. Los peluches japoneses, en particular, son muy conocidos por su estilo tierno y detallado, y algunas marcas famosas como San-X o Sanrio han creado personajes icónicos, como Rilakkuma y Hello Kitty. Además de ser juguetes, los peluches se utilizan como artículos de colección o decoración, y su aspecto es generalmente colorido y amigable.', '2025-06-12 07:06:02.983988'),
(5, 'Juegos de mesa', 'Los juegos de mesa son juegos que se juegan sobre una superficie plana, normalmente una mesa, y que implican piezas, cartas o tableros. Pueden ser de estrategia, azar o una combinación de ambos, y están diseñados para ser jugados en grupo, lo que fomenta la interacción social. Algunos ejemplos populares incluyen Monopoly, Ajedrez, Catan y Risk. Los juegos de mesa varían en complejidad, desde juegos sencillos para niños hasta juegos más estratégicos para adultos. También existen juegos de mesa basados en licencias de anime o películas, como Dragon Ball Super: Card Game o One Piece: Pirate’s Plunder, que añaden un toque temático para los fanáticos.', '2025-06-12 07:06:10.693327'),
(6, 'Posters', 'Los pósters son impresiones gráficas que representan imágenes, escenas o personajes, comúnmente de series de anime, manga o videojuegos. Generalmente están impresos en papel satinado o mate, y pueden variar en tamaño desde pequeños A4 hasta formatos grandes para decoración mural. Son populares entre los fanáticos por su capacidad de ambientar habitaciones con estilo temático. Algunos pósters presentan ilustraciones oficiales, mientras que otros ofrecen arte exclusivo de edición limitada. Además de su función decorativa, los pósters pueden ser objetos de colección valorados por su rareza o diseño artístico.', '2025-06-12 07:06:16.820438'),
(7, 'Llaveros', 'Los llaveros son pequeños accesorios decorativos que suelen colocarse en llaves, mochilas o estuches. En el mundo del anime, los llaveros representan personajes, símbolos o elementos icónicos de una serie, y están fabricados en materiales como acrílico, goma PVC, metal o felpa. Su tamaño compacto los hace ideales como recuerdo o regalo, y pueden ser parte de sets temáticos o lanzamientos especiales. Algunos incluyen funciones adicionales como luces o sonido. Son muy apreciados por su practicidad, diseño atractivo y bajo costo, lo que los hace ideales para coleccionistas casuales o entusiastas.', '2025-06-12 07:06:23.690985'),
(8, 'Papelería', 'La papelería temática de anime incluye cuadernos, libretas, lápices, lapiceras, stickers, carpetas y otros materiales escolares o de oficina decorados con personajes y escenas de anime. Estos productos combinan funcionalidad con estilo, y son especialmente populares entre estudiantes, artistas y coleccionistas. Muchas veces vienen en sets temáticos o en presentaciones especiales. La papelería de anime es conocida por su calidad visual, colores vivos y atención al detalle, haciendo que escribir, dibujar o estudiar sea una experiencia más entretenida.', '2025-06-12 07:06:29.244933'),
(9, 'Puzzles', 'Los puzzles de anime son rompecabezas ilustrados con escenas, personajes o arte oficial de series japonesas. Pueden ir desde 300 hasta más de 1000 piezas, y están diseñados tanto para niños como para adultos. Armar un puzzle no solo es una actividad relajante, sino también una forma de interactuar con tu serie favorita de manera diferente. Una vez completados, muchos fanáticos los enmarcan como piezas decorativas. Los puzzles de anime también pueden formar parte de colecciones exclusivas o lanzamientos especiales que destacan por su diseño y dificultad.', '2025-06-12 07:06:40.212738'),
(10, 'Prendas', 'Estas prendas están inspiradas directamente en los atuendos icónicos de personajes de anime, como las haoris de Demon Slayer, los uniformes escolares de My Hero Academia o los trajes ninja de Naruto. Son réplicas fieles hechas con materiales ligeros y cómodos, ideales tanto para cosplay como para uso casual. Cada diseño refleja los detalles únicos del personaje, desde los patrones de tela hasta los colores y símbolos característicos. Estas túnicas y trajes permiten a los fanáticos vestir como sus héroes favoritos y destacar en eventos, convenciones o en su día a día con un toque auténtico de estilo anime.', '2025-06-12 07:06:56.631828'),
(11, 'Bebidas', 'Las bebidas japonesas ofrecen una experiencia refrescante y única, con sabores que van desde lo tradicional hasta lo más innovador. En esta categoría encontrarás refrescos, tés, jugos y bebidas energéticas que muchas veces están decoradas con personajes de anime o tienen envases temáticos de series populares. Algunas de las más conocidas incluyen las sodas Ramune, bebidas de matcha, y cafés enlatados. Muchas de estas bebidas vienen en ediciones limitadas o coleccionables, y destacan por sus envases coloridos y sabores poco comunes como uva japonesa, melón, lychee o durazno blanco. Son perfectas para acompañar un snack o como regalo original para fanáticos del anime y la cultura japonesa.', '2025-06-12 07:07:04.674869'),
(12, 'Ramen', 'El Ramen japonés es uno de los platos más icónicos y queridos de la gastronomía japonesa. Con su combinación de fideos suaves, un caldo rico y sabroso, y una variedad de toppings, el ramen es perfecto para cualquier ocasión. Desde ramen instantáneo para una comida rápida hasta ramen tradicional hecho en casa, hay algo para todos los gustos. En nuestra tienda, ofrecemos una amplia selección de ramen que incluye opciones como ramen de cerdo, ramen de pollo, y ramen picante. Para aquellos que buscan alternativas sin carne, también contamos con ramen vegetariano que no sacrifica el sabor. Si deseas aprender a preparar ramen fácil de hacer, nuestros productos incluyen instrucciones paso a paso para hacer el ramen casero instantáneo y rápido. Ya sea que prefieras ramen de miso, ramen de soya, o una deliciosa mezcla de sabores, tenemos todo lo que necesitas para llevar la experiencia del ramen a tu cocina.', '2025-06-12 22:22:55.731838');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sysapp_producto`
--

CREATE TABLE `sysapp_producto` (
  `id` bigint(20) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `precio` int(11) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `descripcion` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sysapp_producto`
--

INSERT INTO `sysapp_producto` (`id`, `titulo`, `precio`, `foto`, `stock`, `categoria_id`, `descripcion`) VALUES
(2, 'Peluche Pokemon 8\" Quaxly Jazwares', 24990, 'productos/Peluche_Pokemon_8_Quaxly_Jazwares.jpeg', 14, 4, 'Peluche Pokemon 8&quot; Quaxly Jazwares\r\nPeluche Pokemon 8&quot; Quaxly Jazwarez\r\nPeluche Pokemon 8&quot; Quaxly Jazwarez\r\nPeluche Pokemon 8&quot; Quaxly Jazwarez\r\nPeluche Pokemon 8&quot; Quaxly Jazwarez\r\nPeluche Pokemon 8&quot; Quaxly Jazwarez\r\nPeluche Pokemon 8\" Quaxly Jazwares\r\n STOCK\r\nMateriales suaves: Fabricado con tela de alta calidad, ideal para abrazar y disfrutar.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Quaxly en la serie animada de Pokémon.\r\n\r\nTamaño compacto: Con una altura de aproximadamente 20 cm, es perfecto para llevar contigo o exhibir en tu colección.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.'),
(3, 'Peluche Pokemon 8\" Fuecoco Jazwares', 24990, 'productos/image.jpeg', 1, 4, 'Materiales suaves: Fabricado con tela de alta calidad, ideal para abrazar y disfrutar.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Fuecoco en la serie animada de Pokémon.\r\n\r\nTamaño compacto: Con una altura de aproximadamente 20 cm, es perfecto para llevar contigo o exhibir en tu colección.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.'),
(4, 'Peluche Pokemon 12 Dragonair Jazwares', 29990, 'productos/image_1.jpeg', 15, 4, 'Materiales ultra suaves: Fabricado con tela de alta calidad, ideal para disfrutar de abrazos y comodidad.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Dragonair en la serie animada de Pokémon.\r\n\r\nTamaño extra: Con una longitud de aproximadamente 30 cm, este peluche es perfecto para destacar en tu colección o como decoración especial.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.\r\n\r\nREF: 191726481881'),
(5, 'Peluche Pokemon 12 Eevee Jazwares', 29990, 'productos/image_2.jpeg', 0, 4, 'Materiales ultra suaves: Diseñado con tela de alta calidad para garantizar abrazos confortables y una textura agradable.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Eevee tal como lo conocemos de la serie y los videojuegos.\r\n\r\nTamaño extra: Con 12 pulgadas (aproximadamente 30 cm) de altura, este peluche destaca como pieza central en cualquier colección o como un compañero para abrazos.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, lo que asegura su autenticidad y alta calidad.\r\n\r\nREF: 191726481850'),
(6, 'Peluche Pokemon 12 Pikachu Jazwares', 29990, 'productos/image_3.jpeg', 4, 4, 'Materiales ultra suaves: Diseñado con tela de alta calidad para garantizar abrazos confortables y una textura agradable.\r\n\r\nDiseño auténtico: Detalles precisos que capturan a la perfección la apariencia de Pikachu tal como lo conocemos de la serie y los videojuegos.\r\n\r\nTamaño extra: Con 12 pulgadas (aproximadamente 30 cm) de altura, este peluche destaca como pieza central en cualquier colección o como un compañero para abrazos.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, lo que asegura su autenticidad y alta calidad.\r\n\r\nREF: 191726481867'),
(7, 'Peluche Pokemon 8\" Flareon Jazwares', 24990, 'productos/image_4.jpeg', 9, 4, 'Diseño exclusivo: Representación fiel de Flareon, con acabados premium.\r\n\r\nMaterial premium: Fabricado en felpa ultra suave, garantizando comodidad y calidad.\r\nDimensiones: Altura aproximada de 20 cm, ideal para exhibición o juego.\r\nLicencia oficial: Producto con certificación de Pokémon y Jazwares.\r\nREF: 191726507222'),
(8, 'Peluche Pokemon 8&quot; Squirtle Jazwares', 24990, 'productos/image_6.jpeg', 0, 4, 'Materiales suaves: Fabricado con tela de alta calidad, ideal para abrazar y disfrutar.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Squirtle en la serie animada de Pokémon.\r\n\r\nTamaño compacto: Con una altura de aproximadamente 20 cm, es perfecto para llevar contigo o exhibir en tu colección.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.\r\n\r\nREF: 191726483403'),
(9, 'Peluche Pokemon 8\" Charmander Jazwares', 24990, 'productos/image_7.jpeg', 8, 4, 'Materiales suaves: Fabricado con tela de alta calidad, ideal para abrazar y disfrutar.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Charmander en la serie animada de Pokémon.\r\n\r\nTamaño compacto: Con una altura de aproximadamente 20 cm, es perfecto para llevar contigo o exhibir en tu colección.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.\r\n\r\nREF: 191726483410'),
(10, 'Peluche Pokemon 8&quot; Pikachu', 24990, 'productos/image_8.jpeg', 16, 4, 'Materiales suaves: Fabricado con tela de alta calidad, ideal para abrazar y disfrutar.\r\n\r\nDiseño auténtico: Detalles precisos que reflejan la apariencia de Pikachu en la serie animada de Pokémon.\r\n\r\nTamaño compacto: Con una altura de aproximadamente 20 cm, es perfecto para llevar contigo o exhibir en tu colección.\r\n\r\nLicencia oficial: Producto original de Jazwares, fabricado bajo licencia oficial de Pokémon y Nintendo, garantizando autenticidad y calidad.\r\n\r\nREF: 191726483380'),
(11, 'Figura Sasuke Mangekyo Sharingan', 75990, 'productos/image_9.jpeg', 10, 1, 'Materiales: PVC, ABS\r\n\r\nAltura: 20 cm\r\n\r\nAccesorios incluidos: Efectos de batalla adicionales\r\n\r\nMarca: Tamashii Nations\r\n\r\nFabricante: Bandai\r\n\r\nInspiración: Naruto Shippuden\r\n\r\nREF: 4573102661128'),
(12, 'FIGURA DRAGON BALL VEGETA 24000 PO', 55990, 'productos/image_10.jpeg', 7, 1, 'Tamashii Nations presenta, dentro de la colección S.H Figuarts, la figura de Vegeta 24000 Power Level Version. Está basada en el personaje del anime \"Dragon Ball Z\" y mide 14 cm. Contiene 3x pares de manos, 3 pares de caras, partes opcionales de brazos cruzados, partes opcionales de orejas y 1x scouter extraíble\r\n\r\nContenido:\r\n\r\n- Pares de manos  x 3\r\n- Pares de cara x 3\r\n- Brazos cruzados \r\n- Orejas opcioneles\r\n- Scouter\r\n\r\n\r\nMaterial:\r\n\r\nPVC, ABS\r\n\r\nAltura:\r\n14 cm aprox.\r\n\r\nREF: 4573102661241'),
(13, 'S.H.FIGUARTS SUPER SAIYAN SON GOKU', 31990, 'productos/image_12.jpeg', 18, 1, 'Diseño articulado: Incorpora el nuevo Dynamic-Movable Shoulder System, que mejora la movilidad sin comprometer la silueta.\r\n\r\nDetalles premium: Modelado renovado con proporciones fieles al anime, incluyendo volumen de cabello y expresiones faciales.\r\nAccesorios incluidos: Cuatro pares de manos intercambiables, cabeza alternativa con cabello en movimiento y tres expresiones faciales.\r\nMateriales de calidad: Fabricado con PVC y ABS para garantizar durabilidad y un acabado impecable.\r\nTamaño compacto: Aproximadamente 15 cm de altura, ideal para exhibición.\r\nREF: 4573102676122'),
(14, 'GUNDAM UNIVERSE RX-78-2', 31990, 'productos/image_13.jpeg', 16, 1, 'Diseño articulado: Permite una gran variedad de movimientos para recrear escenas icónicas.\r\n\r\nDetalles premium: Incluye una nueva estructura interna que mejora la movilidad y estabilidad.\r\nAccesorios incluidos: Beam Rifle, Hyper Bazooka, Shield, Gundam Hammer y Beam Javelin.\r\nMateriales de calidad: Fabricado con ABS y PVC para garantizar durabilidad y un acabado impecable.\r\nTamaño compacto: Aproximadamente 15 cm de altura, ideal para exhibición.\r\nREF: 4573102676580'),
(15, 'FIGUARTS ZERO CHOUETTE RANMA', 95990, 'productos/image_14.jpeg', 2, 1, 'Diseño detallado: Representa a Ranma con una expresión juguetona y una pose icónica.\r\n\r\nEfectos dinámicos: La base incluye efectos de agua translúcida que evocan la transformación de Ranma.\r\nMateriales de calidad: Fabricado con PVC y ABS para garantizar durabilidad y un acabado impecable.\r\nTamaño compacto: Aproximadamente 20 cm de altura, ideal para exhibición.\r\nLicencia oficial: Producto auténtico de Tamashii Nations, diseñado para coleccionistas.\r\nREF: 4573102676030'),
(16, 'S.H.FIGUARTS CHAINSAW MAN', 55990, 'productos/image_15.jpeg', 12, 1, 'Diseño articulado: Permite una gran variedad de movimientos para recrear escenas icónicas.\r\n\r\nDetalles premium: Incluye una nueva estructura interna que mejora la movilidad y estabilidad.\r\nAccesorios incluidos: Manos intercambiables, piezas de expresión facial y efectos de acción.\r\nMateriales de calidad: Fabricado con PVC y ABS para garantizar durabilidad y un acabado impecable.\r\nTamaño compacto: Aproximadamente 15 cm de altura, ideal para exhibición.\r\nREF: 4573102687258'),
(17, 'FIGURA ACCION SHY S.H.Figuarts Tamashii Nations', 67990, 'productos/image_16.jpeg', 1, 1, 'Materiales: PVC, ABS\r\n\r\nAltura: 12,5 cm\r\n\r\nAccesorios incluidos: Cuatro expresiones faciales opcionales, tres manos izquierdas y seis derechas intercambiables, parte de cabello opcional, parte del capó opcional\r\n\r\nMarca: Tamashii Nations\r\n\r\nFabricante: Bandai\r\n\r\nInspiración: Anime Shy\r\n\r\nREF: 4573102661821'),
(18, 'DESTINED RIVALS BOOSTERS ESPAÑOL POKEMON COMPANY', 5490, 'productos/image_18.jpeg', 40, 2, 'POKEMON COMPANY\r\nMás de 240 cartas nuevas, incluyendo Pokémon de Entrenador y del Equipo Rocket.\r\n\r\n17 Pokémon ex, con 10 Pokémon ex de Entrenador.\r\nMás de 45 cartas con ilustraciones especiales.\r\nIdioma: Español.'),
(19, 'DESTINED RIVALS BOOSTERS INGLÉS POKEMON COMPANY', 5990, 'productos/image_19.jpeg', 16, 2, 'POKEMON COMPANY\r\nMás de 240 cartas nuevas, incluyendo Pokémon de Entrenador y del Equipo Rocket.\r\n\r\n17 Pokémon ex, con 10 Pokémon ex de Entrenador.\r\nMás de 45 cartas con ilustraciones especiales.\r\nFecha de lanzamiento: 30 de mayo de 2025.'),
(20, 'POKEMON TCG SCARLET & VIOLET - DESTINED RIVALS BOOSTER BUNDLE ENGLISH POKEMON COMPANY', 35990, 'productos/image_20.jpeg', 2, 2, 'POKEMON COMPANY\r\nMás de 240 cartas nuevas, incluyendo Pokémon de Entrenador y del Equipo Rocket.\r\n\r\n17 Pokémon ex, con 10 Pokémon ex de Entrenador.\r\nMás de 45 cartas con ilustraciones especiales.\r\nIncluye 6 sobres de la expansión Destined Rivals.\r\nIdioma: Inglés.'),
(21, 'POKEMON TCG SCARLET & VIOLET - DESTINED RIVALS 3- PACK BLISTER ENGLISH POKEMON COMPANY', 18990, 'productos/image_21.jpeg', 7, 2, 'POKEMON COMPANY\r\nMás de 240 cartas nuevas, incluyendo Pokémon de Entrenador y del Equipo Rocket\r\n\r\n17 Pokémon ex, con 10 Pokémon ex de Entrenador\r\nMás de 45 cartas con ilustraciones especiales\r\nIncluye 3 sobres de la expansión Destined Rivals y una carta promocional exclusiva.\r\nIdioma: Inglés.'),
(22, 'LILLIE PREMIUM TOURNAMENT COLLECTION INGLÉS POKEMON COMPANY LILLIE PREMIUM TOURNAMENT COLLECTION IN', 55990, 'productos/image_22.jpeg', 17, 2, 'POKEMON COMPANY\r\nCartas exclusivas: Incluye 1 carta promocional Full Art de Lillie\'s Clefairy Ex y 3 cartas holográficas de Lillie\'s Pearl.\r\n\r\nAccesorios premium: 65 fundas de carta de Lillie, caja para mazo, moneda metálica y sticker exclusivo.\r\nPaquetes de refuerzo: 6 sobres de la expansión Scarlet & Violet.\r\nCódigo para Pokémon TCG Live: Expande tu colección en el juego digital.\r\nMarcadores y dados: 2 marcadores de condición y 6 dados aptos para torneo.'),
(23, 'PRISMATIC EVOLUTIONS - ACCESSORY POUCH ESPAÑOL POKEMON COMPANY', 39990, 'productos/image_23.jpeg', 16, 2, 'La colección especial con bolsa para accesorios de Escarlata y Púrpura-Evoluciones Prismáticas de JCC Pokémon contiene: \r\n\r\n1 divertida bolsa para accesorios de Eevee\r\n\r\n5 paquetes de mejora de Escarlata y Púrpura-Evoluciones Prismáticas de JCC Pokémon'),
(24, 'COLLECTOR CHEST FALL 2024 ESPAÑOL - POKEMON COMPANY COLLECTOR CHEST FALL 2024 ESPAÑOL - POKEMON COM', 36990, 'productos/image_24.jpeg', 8, 2, '-Contenido:\r\n-6 paquetes de refuerzo Pokémon TCG\r\n-2 cartas de promoción\r\n-2 monedas\r\n-1 mini carpeta\r\n-4 hojas de pegatinas\r\n-1 tarjeta de código'),
(25, 'HOP\'S ZACIAN EX BOX ESPAÑOL - POKEMON COMPANY HOP\'S ZACIAN EX BOX ESPAÑOL - POKEMON COMPANY HOP\'S Z', 25990, 'productos/image_25.jpeg', 2, 2, 'POKEMON COMPANY'),
(26, 'JOURNEY TOGETHER ELITE TRAINER BOX ESPAÑOL - POKEMON COMPANY', 59990, 'productos/image_26.jpeg', 0, 2, 'POKEMON COMPANY'),
(27, 'POLERA CATORU BY LEON LIZAMA NEGRA - GKZ', 19990, 'productos/image_27.jpeg', 20, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Leon Lizama, con detalles inspirados en la cultura pop.\r\n\r\nTécnica de impresión: DTG (Direct to Garment), garantizando nitidez y durabilidad.\r\nMaterial premium: Tejido de 180 g/m², resistente y cómoda.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\nTALLA:\r\nS\r\nCOLOR:\r\nNEGRO'),
(28, 'POLERA SATORU GOJO POLERA BLANCA - JUJUTSU KAISEN - GEEKZ', 19990, 'productos/image_28.jpeg', 14, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Satoru Gojo, con detalles inspirados en Jujutsu Kaisen.\r\n\r\nTécnica de impresión: DTG (Direct to Garment), garantizando colores vibrantes y durabilidad.\r\nMaterial premium: Tejido de 180 g/m² de alta calidad, suave y resistente.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\nTALLA:\r\nS\r\nM\r\nXL\r\nCOLOR:\r\nBLANCO'),
(29, 'POLERA SUKUNA NEGRA REVERSE - JUJUTSU KAISEN - GEEKZ', 19990, 'productos/image_29.jpeg', 28, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Ryomen Sukuna, con detalles inspirados en Jujutsu Kaisen.\r\n\r\nTécnica de impresión: DTF (Direct to Film), garantizando nitidez y durabilidad.\r\nMaterial premium: Tejido de 180 g/m², resistente y cómoda.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\n\r\nTALLA:\r\nS\r\nM\r\nL\r\nXL\r\nCOLOR:\r\nNEGRA'),
(30, 'POLERA NANAMI NEGRA REVERSE - JUJUTSU KAISEN - GEEKZ', 19990, 'productos/image_30.jpeg', 5, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Kento Nanami, con detalles inspirados en Jujutsu Kaisen.\r\n\r\nTécnica de impresión: DTF (Direct to Film), garantizando nitidez y durabilidad.\r\nMaterial premium: Tejido de 180 g/m², resistente y cómoda.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\nTALLA:\r\nS\r\nL\r\nCOLOR:\r\nNEGRA'),
(31, 'POLERA ZORO BLANCA - ONE PIECE - Geekz', 19990, 'productos/image_31.jpeg', 12, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Roronoa Zoro, con detalles inspirados en One Piece.\r\n\r\nTécnica de impresión: DTG (Direct to Garment), garantizando colores vibrantes y durabilidad.\r\nMaterial premium: Tejido de 180 g/m² de alta calidad, suave y resistente.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\n\r\nTALLA:\r\nS\r\nM\r\nL\r\nXL\r\nCOLOR: \r\nBLANCA'),
(33, 'POLERA USOPP BLANCA- ONE PIECE - Geekz', 19990, 'productos/image_32.jpeg', 5, 10, 'GKZ STUDIO\r\nDiseño exclusivo: Estampado de Usopp, con detalles inspirados en One Piece.\r\n\r\nTécnica de impresión: DTF (Direct to Film), garantizando colores vibrantes y durabilidad.\r\nMaterial premium: Tejido de 180 g/m² de alta calidad, suave y resistente.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\nTALLA:\r\nS\r\nM\r\nL\r\nXL\r\nCOLOR:\r\nBLANCA'),
(34, 'POLERA SANJI BLANCA - ONE PIECE - Geekz', 19990, 'productos/image_33.jpeg', 15, 10, 'KZ STUDIO\r\nDiseño exclusivo: Estampado de Sanji, con detalles inspirados en One Piece.\r\n\r\nTécnica de impresión: DTF (Direct to Film), garantizando colores vibrantes y durabilidad.\r\nMaterial premium: Tejido de 180 g/m² de alta calidad, suave y resistente.\r\nCorte clásico: Ajuste recto, ideal para cualquier ocasión.\r\n\r\nTALLA:\r\nS\r\nM\r\nL\r\nXL\r\nCOLOR:\r\nBLANCA'),
(35, 'Ocean Bomb de granada edición Digimon (Gatomon)', 2500, 'productos/4712966543076.jpg', 25, 11, 'Ocean Bomb de Granada Edición Digimon (Gatomon)\r\n\r\n¡Sumérgete en el mundo digital con Ocean Bomb Edición Digimon (Gatomon)! Este refresco de granada te lleva directamente al universo de Digimon con su diseño inspirado en el adorable Gatomon. Disfruta de un sabor refrescante y revitalizante mientras revives tus recuerdos de la serie.\r\n\r\nSabor Frutal de Granada: Disfruta de la deliciosa y refrescante explosión de sabor de la granada en cada sorbo.\r\n\r\nEdición Especial Digimon: Presenta un diseño temático de Gatomon, añadiendo nostalgia y emoción a tu experiencia.\r\n\r\nSin Cafeína: Ideal para disfrutar en cualquier momento del día sin preocupaciones por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborado con ingredientes premium para garantizar un sabor auténtico y fresco.\r\n\r\nBotella Coleccionable: Conserva la botella como un recuerdo de tus aventuras en el mundo digital.\r\n\r\nMaratón de Digimon: Acompaña tus maratones de Digimon con este refresco temático para una experiencia aún más emocionante.\r\n\r\nDescanso en Casa: Disfruta de un momento de relax en casa con el refrescante sabor de la granada inspirado en Gatomon.\r\n\r\nSesiones de Juegos: Recarga energías durante tus sesiones de juego con esta bebida revitalizante y llena de nostalgia.\r\n\r\n¡Revive la emoción de Digimon con Ocean Bomb Edición Granada! Disfruta del sabor refrescante de la granada mientras te sumerges en el mundo de los Digimon junto a Gatomon. Perfecto para los fanáticos del anime y los nostálgicos que buscan una experiencia de sabor única y emocionante.'),
(36, 'Ocean Bomb de banana edición Digimon (Agumon)', 2500, 'productos/4712966543052.jpg', 15, 11, 'Ocean Bomb de Banana Edición Digimon (Agumon)\r\n\r\n¡Embárcate en una aventura emocionante con Ocean Bomb Edición Digimon (Agumon)! Este refresco de banana te transporta al mundo de Digimon con su diseño inspirado en el querido Agumon. Disfruta de un sabor refrescante y delicioso mientras revives tus recuerdos de la serie.\r\n\r\nSabor Dulce de Banana: Disfruta de la deliciosa y refrescante explosión de sabor a banana en cada sorbo.\r\n\r\nEdición Especial Digimon: Presenta un diseño temático de Agumon, agregando un toque de nostalgia y emoción a tu experiencia.\r\n\r\nSin Cafeína: Ideal para disfrutar en cualquier momento del día sin preocupaciones por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborado con ingredientes premium para garantizar un sabor auténtico y fresco.\r\n\r\nBotella Coleccionable: Conserva la botella como un recuerdo de tus aventuras en el mundo digital.\r\n\r\nMaratón de Digimon: Acompaña tus maratones de Digimon con este refresco temático para una experiencia aún más emocionante.\r\n\r\nDescanso en Casa: Disfruta de un momento de relax en casa con el refrescante sabor a banana inspirado en Agumon.\r\n\r\nSesiones de Juegos: Recarga energías durante tus sesiones de juego con esta bebida revitalizante y llena de nostalgia.\r\n\r\n¡Revive la emoción de Digimon con Ocean Bomb Edición Banana! Disfruta del sabor refrescante de la banana mientras te sumerges en el mundo de los Digimon junto a Agumon. Perfecto para los fanáticos del anime y los nostálgicos que buscan una experiencia de sabor única y emocionante.'),
(37, 'Ocean Bomb de limón edición Digimon (Patamon)', 2500, 'productos/4712966543083.jpg', 5, 11, 'Ocean Bomb de Limón Edición Digimon (Patamon)\r\n\r\n¡Embárcate en una aventura refrescante con Ocean Bomb Edición Digimon (Patamon)! Este refresco de limón te lleva de vuelta al mundo de Digimon con su diseño inspirado en el adorable Patamon. Disfruta de un sabor cítrico y delicioso mientras revives tus recuerdos de la serie.\r\n\r\nSabor Cítrico de Limón: Disfruta de la explosión refrescante y ácida del limón en cada sorbo.\r\n\r\nEdición Especial Digimon: Presenta un diseño temático de Patamon, agregando un toque de nostalgia y emoción a tu experiencia.\r\n\r\nSin Cafeína: Ideal para disfrutar en cualquier momento del día sin preocupaciones por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborado con ingredientes premium para garantizar un sabor auténtico y fresco.\r\n\r\nBotella Coleccionable: Conserva la botella como un recuerdo de tus aventuras en el mundo digital.\r\n\r\nMaratón de Digimon: Acompaña tus maratones de Digimon con este refresco temático para una experiencia aún más emocionante.\r\n\r\nDescanso en Casa: Disfruta de un momento de relax en casa con el refrescante sabor a limón inspirado en Patamon.\r\n\r\nSesiones de Juegos: Recarga energías durante tus sesiones de juego con esta bebida revitalizante y llena de nostalgia.\r\n\r\n¡Revive la emoción de Digimon con Ocean Bomb Edición Limón! Disfruta del sabor refrescante del limón mientras te sumerges en el mundo de los Digimon junto a Patamon. Perfecto para los fanáticos del anime y los nostálgicos que buscan una experiencia de sabor única y emocionante.'),
(38, 'Ocean Bomb de kiwi edición Sailor Moon (Michiru Kaio)', 2500, 'productos/4712966542758.jpg', 10, 11, 'Ocean Bomb Kiwi Edición Sailor Moon (Michiru Kaio) – Bebida Refrescante de Taiwán\r\n\r\nDescubre la Ocean Bomb de kiwi edición Sailor Moon, una bebida refrescante y dulce de edición limitada inspirada en la popular serie de anime Sailor Moon. Presentada en una lata de 330ml, esta bebida tiene un delicioso sabor a kiwi, conocido por su frescura y dulzura característica.\r\n\r\nSabor Auténtico: Disfruta de un sabor auténtico de kiwi, elaborado con agua mineral y pulpa de kiwi.\r\nIngredientes de Calidad: Agua carbonatada, fructosa, azúcar, aroma natural, antioxidante (E330).\r\nEdición Limitada Sailor Moon: Lata decorada con diseño impresionante de Sailor Moon y Michiru Kaio.\r\nInformación Nutricional por 100ml: 31 kcal, 0g de proteínas, 0g de grasas, 0g de carbohidratos, 0,02g de sal.\r\nSin Grasas ni Conservantes: Opción saludable y refrescante para todos los consumidores.\r\nOrigen: Producida en Taiwán con estándares de calidad y frescura garantizados.\r\nPara Coleccionistas: Ideal para fans de Sailor Moon que buscan artículos de colección únicos.\r\nRefrescante y Delicioso: Perfecto para disfrutar en cualquier momento del día, especialmente en días calurosos.\r\nSaludable y Natural: Elaborado con ingredientes naturales y sin aditivos artificiales.\r\n\r\nNo te pierdas la oportunidad de probar esta exclusiva Ocean Bomb de kiwi edición Sailor Moon. Añádela a tu colección de bebidas o disfrútala como una opción refrescante y sabrosa.'),
(39, 'Ocean Bomb de uvas rojas edición Boku No Hero (Katsuki Bakugo)', 2500, 'productos/4712966543199.jpg', 13, 11, 'Ocean Bomb Uvas Rojas Edición Boku No Hero (Katsuki Bakugo)\r\n\r\n¡Prepárate para una explosión de sabor con Ocean Bomb Edición Boku No Hero (Katsuki Bakugo)! Este refresco de uvas rojas te sumergirá en el mundo de My Hero Academia con un diseño inspirado en el poderoso Katsuki Bakugo. Disfruta de un sabor delicioso y refrescante mientras te sumerges en el universo de tus héroes favoritos.\r\n\r\nSabor Intenso: Disfruta del dulce y refrescante sabor de las uvas rojas en cada sorbo, una explosión de frescura y sabor.\r\n\r\nEdición Especial Boku No Hero: Presenta un diseño temático de Katsuki Bakugo, añadiendo emoción y autenticidad a tu experiencia.\r\n\r\nSin Cafeína: Ideal para disfrutar en cualquier momento del día sin preocupaciones por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborada con ingredientes de alta calidad para garantizar un sabor auténtico y fresco.\r\n\r\nBotella Coleccionable: Conserva la botella como un artículo de colección después de disfrutar de la bebida.\r\n\r\nSesiones de Anime: Acompaña tus maratones de Boku No Hero con este refresco temático para una experiencia aún más inmersiva.\r\n\r\nReuniones con Amigos: Sorprende a tus amigos fanáticos de My Hero Academia con esta edición especial mientras disfrutan de la serie juntos.\r\n\r\nMomentos de Relax: Refréscate y recarga energías con el delicioso sabor de las uvas rojas después de un día agotador.\r\n\r\n¡Sumérgete en el mundo de Boku No Hero con Ocean Bomb Edición Katsuki Bakugo! Disfruta del refrescante sabor de las uvas rojas en esta edición especial inspirada en uno de los personajes más poderosos de la serie. Perfecta para fanáticos del anime y amantes de los sabores intensos.'),
(40, 'cean Bomb de frambuesa edición One Piece (Law)', 2500, 'productos/4712966543373.jpg', 7, 11, 'Ocean Bomb de Frambuesa Edición One Piece (Law)\r\n\r\n¡Prepárate para una aventura pirata con Ocean Bomb Edición One Piece de Frambuesa, dedicada al intrépido Trafalgar Law! Este refresco combina el sabor dulce y refrescante de la frambuesa con una explosión de energía digna de un verdadero pirata.\r\n\r\nSabor Intenso de Frambuesa: Disfruta de la jugosidad y el dulzor natural de las frambuesas en cada sorbo.\r\n\r\nEdición Especial One Piece: Presenta un diseño temático de Trafalgar Law, agregando un toque de piratería y aventura a tu experiencia.\r\n\r\nSin Cafeína: Ideal para disfrutar en cualquier momento del día sin preocuparte por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborado con ingredientes premium para garantizar un sabor auténtico y refrescante.\r\n\r\nBotella Coleccionable: Conserva la botella como un tesoro de tus aventuras junto a Trafalgar Law\r\n\r\nNavegando por los Mares: Refréscate con Ocean Bomb mientras navegas por los mares del Grand Line en busca del One Piece.\r\n\r\nFiestas Piratas: Celebra con tus amigos con este refresco temático que agregará emoción a tus fiestas.\r\n\r\nMomentos de Relax: Disfruta de un momento de relax en la cubierta del barco con este refresco tropical y refrescante.\r\n\r\n¡Zarpa hacia aventuras piratas con Ocean Bomb Edición One Piece de Frambuesa! Disfruta del dulce sabor de la frambuesa y la emoción de la piratería con cada sorbo mientras te unes a Trafalgar Law en su búsqueda del tesoro más grande. Perfecto para los amantes de One Piece y quienes buscan una experiencia refrescante llena de sabor y emoción.'),
(41, 'Ocean Bomb de melocotón edición Boku No Hero (Izuku Midoriya)', 2500, 'productos/4712966543182.jpg', 15, 11, 'Ocean Bomb de Melocotón Edición Boku No Hero (Izuku Midoriya)\r\n\r\n¡Experimenta el poder y la frescura con Ocean Bomb Edición Boku No Hero (Izuku Midoriya)! Este refresco de melocotón te llevará al emocionante mundo de My Hero Academia con un diseño inspirado en el valiente Izuku Midoriya. Disfruta de un sabor delicioso y revitalizante mientras te sumerges en la historia de tus héroes favoritos.\r\n\r\nSabor Dulce de Melocotón: Disfruta de la refrescante y dulce explosión de sabor del melocotón en cada sorbo, una experiencia deliciosa y energizante.\r\n\r\nEdición Especial Boku No Hero: Presenta un diseño temático de Izuku Midoriya, agregando autenticidad y emoción a tu experiencia.\r\n\r\nSin Cafeína: Perfecto para disfrutar en cualquier momento del día sin preocupaciones por la cafeína.\r\n\r\nIngredientes de Calidad: Elaborado con ingredientes de alta calidad para garantizar un sabor auténtico y fresco.\r\n\r\nBotella Coleccionable: Conserva la botella como un artículo de colección después de disfrutar de la bebida.\r\n\r\nSesiones de Estudio: Acompaña tus sesiones de estudio con este refresco temático para sentirte inspirado por el espíritu de Midoriya.\r\n\r\nReuniones con Amigos: Sorprende a tus amigos fanáticos de Boku No Hero con esta edición especial mientras disfrutan de la serie juntos.\r\n\r\nMomentos de Energía: Recarga energías y disfruta de un momento de frescura con el delicioso sabor del melocotón en cualquier momento del día.\r\n\r\n¡Siente el poder de Izuku Midoriya con el refresco Ocean Bomb Edición Melocotón! Disfruta del refrescante sabor dulce mientras te sumerges en el emocionante mundo de Boku No Hero. Perfecto para los amantes del anime y aquellos que buscan un sabor delicioso y revitalizante.'),
(42, 'Refresco UltraPopツ Edición One Piece Sabor Fresa y Lima', 2500, 'productos/3760412583788.webp', 0, 11, 'Refresco UltraPopツ Edición One Piece Sabor Fresa y Lima\r\n\r\n¡Zarpa hacia el sabor con esta explosiva edición especial!\r\n\r\nEmbárcate en una aventura refrescante con el Refresco UltraPopツ Edición One Piece, inspirado en el intrépido Luffy y con un sabor vibrante a fresa y lima. Dulce, ácido y chispeante, este refresco es tan energético y divertido como su protagonista.\r\n\r\n‍☠️ ¿Por qué te va a enganchar?\r\nCombinación frutal irresistible: el dulzor de la fresa se mezcla con la acidez de la lima, creando un sabor tropical que no pasa desapercibido.\r\n\r\nDiseño exclusivo de Luffy: una lata decorada con el carismático capitán de los Sombrero de Paja, perfecta para fans y coleccionistas.\r\n\r\n⚓ Ideal para refrescar tus días: ya sea en pleno verano o durante una sesión de anime, este refresco te lleva directo al Grand Line… ¡del sabor!\r\n\r\nCon el UltraPopツ One Piece Luffy, cada sorbo es una mini aventura.\r\n¡No dejes que se te escape como el One Piece!'),
(43, 'Chicle Marukawa mini edición SPY X FAMILY cantidad 1 + Aña', 1000, 'productos/4902747111727.jpg.webp', 27, 3, 'Chicle Marukawa Mini Edición SPY X FAMILY\r\n\r\nAdéntrate en el emocionante mundo de SPY X FAMILY con los Chicles Marukawa Mini edición especial. Disfruta de estos chicles deliciosos y colecciona los envoltorios temáticos de tus personajes favoritos de la popular serie. Cada bocado es una explosión de sabor que te transportará a las aventuras de esta peculiar familia de espías.\r\n\r\nSabor Irresistible: Disfruta de los intensos sabores de los chicles Marukawa, conocidos por su calidad y durabilidad.\r\nEdición Especial SPY X FAMILY: Presenta envoltorios únicos con los personajes de la serie SPY X FAMILY, haciendo de cada pieza un coleccionable.\r\nTamaño Mini: Perfecto para llevar en el bolsillo o en la mochila, ideal para disfrutar en cualquier momento y lugar.\r\nCalidad Japonesa: Elaborado con los más altos estándares de calidad en Japón, garantizando una experiencia de sabor superior.\r\nIdeal para Fanáticos: Un regalo perfecto para los seguidores de la serie y amantes del anime, así como para aquellos que disfrutan de chicles deliciosos.\r\nSnack Diario: Disfruta de estos chicles como un refrescante snack durante el día.\r\nColección: Perfecto para coleccionistas de merchandising de anime y fanáticos de SPY X FAMILY.\r\nRegalo: Un detalle divertido y único para amigos, familiares o cualquier fanático del anime.\r\n\r\nDisfruta de los Chicles Marukawa Mini edición SPY X FAMILY. Sabores intensos y envoltorios coleccionables de tus personajes favoritos de la serie. Perfecto para fanáticos y coleccionistas. ¡Directamente desde Japón!'),
(44, 'Chicle Coris edición Dragon Ball', 1000, 'productos/4901361001063.jpg.webp', 14, 3, 'Siente el Poder de los Chicles Coris Edición Dragon Ball\r\n\r\n¡Desata tu poder interior con los chicles Coris edición especial Dragon Ball! Estos chicles te llevarán a un viaje lleno de energía y sabor, inspirados en el emocionante mundo de Dragon Ball. Con envases coleccionables que presentan a tus personajes favoritos y un sabor delicioso que te encantará, ¡prepárate para una experiencia de chicle épica!\r\n\r\nSabor Explosivo: Disfruta del intenso sabor de estos chicles que te dará la energía para tus aventuras.\r\nDiseños Inspirados en Dragon Ball: Encuentra a tus personajes favoritos de Dragon Ball en los envases de estos chicles.\r\nIdeal para Coleccionar: Colecciona todos los diseños de envases y hazte con el poder de Dragon Ball.\r\nCalidad Garantizada: Elaborados con ingredientes de alta calidad para una experiencia de chicle satisfactoria.\r\nPara Compartir: Disfruta de estos chicles con amigos mientras revives las emocionantes aventuras de Dragon Ball.\r\nColeccionables: Colecciona todos los diseños de envases y demuestra tu pasión por Dragon Ball.\r\n\r\nSiente el poder de los chicles Coris edición especial Dragon Ball. Con envases inspirados en tus personajes favoritos y un sabor intenso, estos chicles son perfectos para llevar a todas partes y disfrutar en cualquier momento del día. ¡Colecciona todos los diseños y vive la aventura de Dragon Ball!'),
(45, 'Chicles SonoManma Sabor Monster Energy Coris', 1000, 'productos/4901361061203.webp', 5, 3, '¡Haz que tu día sea más emocionante con los Chicles SonoManma Sabor Monster Energy Coris! Estos chicles no solo ofrecen un delicioso sabor a Monster Energy, sino que también son ideales para mantenerte activo y alerta. Con su textura suave y el inconfundible sabor energético, son perfectos para aquellos momentos en los que necesitas un impulso extra. Disfrútalos en cualquier momento del día y transforma tu rutina con cada chicle. ¡Una explosión de energía en tu boca!'),
(46, 'Creps Want Want Sabor Chocolate', 2500, 'productos/4560160773764.webp', 30, 3, 'Descubre las Creps Want Want Sabor Chocolate, una experiencia crujiente y deliciosa que combina finas capas de crepe enrolladas con un cremoso relleno de chocolate. Cada bocado es un equilibrio perfecto entre textura crujiente y dulzura irresistible, pensado para conquistar tu paladar.\r\n\r\nLa magia del chocolate en cada mordisco\r\nSu delicada capa crujiente se funde con el suave relleno de chocolate, ofreciendo una explosión de sabor que transforma cualquier pausa en un momento especial. Un capricho irresistible para los amantes del dulce.\r\n\r\nCalidad y autenticidad garantizada\r\nElaboradas con ingredientes seleccionados, las Creps Want Want Sabor Chocolate son un homenaje a la tradición japonesa de perfeccionar hasta el último detalle, asegurando un sabor genuino y una textura incomparable.\r\n\r\nPerfectas para cualquier ocasión\r\nIdeales como un snack para media mañana, un acompañamiento para el café o un dulce capricho durante el día. Su formato práctico las convierte en la opción perfecta para llevar y disfrutar donde quieras.\r\n\r\nSumérgete en el irresistible sabor de las Creps Want Want Sabor Chocolate, el snack crujiente que te ofrece la combinación perfecta de textura y dulzura. ¡Porque los pequeños placeres siempre saben mejor!'),
(47, 'Taiyaki de Crema de Chocolate', 2500, 'productos/4902757111304.webp', 60, 3, 'Descubre el Taiyaki de Crema de Chocolate, el icónico dulce japonés en forma de pez que combina tradición y un relleno irresistible.\r\n\r\nUna delicia crujiente y cremosa\r\nSu masa esponjosa y ligeramente crujiente envuelve una suave crema de chocolate, creando un equilibrio perfecto entre textura y sabor en cada bocado.\r\n\r\nAutenticidad japonesa\r\nInspirado en el tradicional taiyaki, este dulce está elaborado con ingredientes de alta calidad para ofrecerte una experiencia genuina de la repostería japonesa.\r\n\r\nPerfecto para cualquier momento\r\nIdeal para acompañar tu merienda, disfrutar en un descanso dulce o sorprender a alguien especial con un capricho delicioso y único.\r\n\r\nDéjate conquistar por el Taiyaki de Crema de Chocolate, una fusión irresistible de tradición y sabor que convierte cualquier instante en una experiencia dulce y especial. 🍫'),
(48, 'Maruchan Mennosuke Katsune Udon', 3000, 'productos/4901990375191.webp', 45, 12, 'Ramen Maruchan Mennosuke Kitsune Udon – Sabor tradicional con alma japonesa\r\n\r\nSumérgete en la calidez de la cocina nipona con el Ramen Maruchan Mennosuke Kitsune Udon, una deliciosa versión del clásico udon con todo el sabor reconfortante del auténtico Japón. Este ramen combina ingredientes típicos de la gastronomía japonesa para ofrecerte una experiencia suave, sabrosa y absolutamente nostálgica.'),
(49, 'Ramen Nissin Sabor Gambas con Salsa de Soja y Pimienta', 3000, 'productos/5997523315450.webp', 31, 12, 'Ramen Nissin Sabor Gambas con Salsa de Soja y Pimienta\r\n\r\nDescubre el delicioso Ramen Nissin Sabor Gambas con Salsa de Soja y Pimienta! ✨ Esta increíble combinación fusiona el intenso y sabroso gusto de las gambas con el toque umami de la salsa de soja y un sutil toque de pimienta, creando un caldo aromático y lleno de carácter. Sus fideos de textura perfecta absorben todos los matices del caldo, ofreciendo una experiencia gastronómica única en cada bocado. Fácil y rápido de preparar, es ideal para quienes buscan disfrutar del auténtico sabor japonés en casa. ¡Déjate llevar por esta explosión de sabores y vive un momento de puro placer!'),
(50, 'Ramen Nissin Sabor Ternera con Salsa Aromática Picante', 3000, 'productos/5997523315412.webp', 10, 12, 'Ramen Nissin Sabor Ternera con Salsa Aromática Picante\r\n\r\n¡Déjate conquistar por el intenso sabor del Ramen Nissin Sabor Ternera con Salsa Aromática Picante! Este ramen combina la suavidad y jugosidad de la ternera con un caldo profundo y lleno de umami, realzado con una salsa aromática y un toque picante que eleva cada bocado. Sus fideos se impregnan perfectamente de la intensidad del caldo, ofreciendo una experiencia reconfortante y deliciosa. Ideal para los amantes de los sabores especiados y auténticamente japoneses. ¡Prepáralo en minutos y disfruta de un ramen lleno de sabor y carácter!'),
(51, 'Ramen Sapporo Ichiban Sabor Marisco Edición Pokémon', 3500, 'productos/4901734024064.webp', 15, 12, '⚡ Ramen Sapporo Ichiban Sabor Marisco – Edición Pokémon ✨\r\n\r\n¡Disfruta de una aventura de sabor con el Ramen Sapporo Ichiban Sabor Marisco, en su encantadora edición especial Pokémon! Esta versión única del clásico ramen japonés combina un delicioso caldo marino con el universo adorable de Pikachu y sus amigos.'),
(52, 'Yakisoba Ippeichan con mantequilla y huevas de bacalao', 3500, 'productos/4902881454728-1.webp', 38, 12, 'Yakisoba Ippeichan con Mantequilla y Huevas de Bacalao\r\n\r\nExperimenta un auténtico festín de sabores con el Yakisoba Ippeichan con Mantequilla y Huevas de Bacalao. Este plato japonés clásico ofrece una combinación irresistible de fideos salteados con mantequilla cremosa y huevas de bacalao para una experiencia culinaria única y deliciosa.\r\n\r\nFideos Salteados: Los fideos Yakisoba tienen una textura firme y un sabor delicioso, perfectamente salteados para realzar su sabor.\r\n\r\nMantequilla Cremosa: La mantequilla añade una riqueza suave y cremosa al plato, complementando perfectamente el sabor de los fideos.\r\n\r\nHuevas de Bacalao: Las huevas de bacalao aportan un toque salado y un estallido de sabor marino que eleva la experiencia gastronómica.\r\n\r\nSabor Auténtico: Preparado con ingredientes de calidad y siguiendo las recetas tradicionales japonesas para un auténtico sabor casero.\r\n\r\nListo en Minutos: Una comida rápida y satisfactoria que puedes disfrutar en cualquier momento, perfecta para los días ocupados.\r\n\r\nPara los Amantes de la Comida Japonesa: Ideal para aquellos que disfrutan de los sabores auténticos de la cocina japonesa.\r\n\r\nComida Rápida y Deliciosa: Perfecto para una comida rápida y satisfactoria en casa o en el trabajo.\r\n\r\nExplora Nuevos Sabores: Una manera emocionante de disfrutar de una combinación única de ingredientes en un plato clásico japonés.\r\n\r\nDisfruta de la combinación perfecta de sabores en el Yakisoba Ippeichan con Mantequilla y Huevas de Bacalao. Fideos salteados con mantequilla cremosa y huevas de bacalao que ofrecen una experiencia culinaria auténtica y deliciosa. ¡Preparado en minutos para satisfacer tus antojos de comida japonesa en cualquier momento del día!'),
(53, 'Ramen Picante Myojo Charmera', 5000, 'productos/4902881456173.webp', 11, 12, 'Ramen Picante Myojo Charmera – Sabor intenso y auténtico desde Japón\r\n\r\n¿Listo para un viaje de sabor que hará latir tu corazón más rápido? El Ramen Picante Myojo Charmera es la opción perfecta para los amantes del ramen que buscan una experiencia con carácter y un toque picante inconfundible.'),
(54, 'Cuaderno Universitario Anime', 2500, 'productos/VI10981_610x_crop_center.webp', 45, 8, '¡Organiza tus apuntes con estilo! El Cuaderno Universitario Anime te ofrece una manera divertida y creativa de mantener tus notas en orden. Con su diseño de anime único, te sentirás inspirado cada vez que lo uses. ¡Haz que estudiar sea más emocionante con este cuaderno!\r\n\r\nModelos Surtidos'),
(55, 'Cuaderno - Jujutsu Kaisen', 3000, 'productos/610.webp', 17, 8, 'Tamaño Normal: 21x15cm\r\n\r\nTamaño Grande: 25x16,6cm\r\n\r\n100 hojas cuadriculadas\r\nAnillos metálicos\r\nElástico'),
(56, 'Cuaderno - Hunter x Hunter', 3000, 'productos/610_1.webp', 2, 8, 'Tamaño Normal: 21x15cm\r\n\r\nTamaño Grande: 25x16,6cm\r\n\r\n100 hojas cuadriculadas\r\nAnillos metálicos\r\nElástico'),
(57, 'Cuaderno - Kimetsu no Yaiba', 3000, 'productos/610_2.webp', 12, 8, 'Tamaño Normal: 21x15cm\r\n\r\nTamaño Grande: 25x16,6cm\r\n\r\n100 hojas cuadriculadas\r\nAnillos metálicos\r\nElástico'),
(58, 'Cuaderno - Boku no Hero', 3000, 'productos/610_3.webp', 0, 8, 'Tamaño Normal: 21x15cm\r\n\r\nTamaño Grande: 25x16,6cm\r\n\r\n100 hojas cuadriculadas\r\nAnillos metálicos\r\nElástico'),
(59, 'Cuaderno - Jibaku Shōnen Hanako-kun', 3000, 'productos/610_4.webp', 14, 8, 'Tamaño Normal: 21x15cm\r\n\r\nTamaño Grande: 25x16,6cm\r\n\r\n100 hojas cuadriculadas\r\nAnillos metálicos\r\nElástico'),
(60, 'Póster Adhesivo - Jujutsu Kaisen', 1500, 'productos/610_5.webp', 20, 6, 'Imagen impresa en papel fotográfico adhesivo \r\n\r\nTamaños: \r\n\r\n21x29.7cm\r\n\r\n29.7x42cm\r\n\r\n32,9 x 48cm'),
(61, 'Póster Adhesivo - Jujutsu Kaisen', 1500, 'productos/610_6.webp', 2, 6, 'Imagen impresa en papel fotográfico adhesivo\r\n\r\nTamaños:\r\n\r\n21x29.7cm\r\n\r\n29.7x42cm\r\n\r\n32,9 x 48cm'),
(62, 'Póster Adhesivo - Cyberpunk: Edgerunners', 1500, 'productos/610_7.webp', 12, 6, 'Imagen impresa en papel fotográfico adhesivo\r\n\r\nTamaños:\r\n\r\n21x29.7cm\r\n\r\n29.7x42cm\r\n\r\n32,9 x 48cm'),
(63, 'Póster Adhesivo - Chainsaw Man', 1500, 'productos/610_8.webp', 3, 6, 'Imagen impresa en papel fotográfico adhesivo\r\n\r\nTamaños:\r\n\r\n21x29.7cm\r\n\r\n29.7x42cm\r\n\r\n32,9 x 48cm'),
(64, 'My Hero Academia Plus Ultra, Juego de Estrategia para Adultos y Adolescentes', 30000, 'productos/81oQbaz5UwL._AC_SY355_.jpg', 0, 5, 'Lleva la clase 1-A a tu mesa: ¡en el My Hero Academia Plus Ultra! Juego de mesa, tú y los otros jugadores controlarán a los estudiantes de U.A. Clase alta 1-A. ¡Demuestra que tienes lo que se necesita para ser un héroe profesional!\r\nJuego de mesa de estrategia: demuestra que tienes lo que se necesita para ser un héroe profesional ganando puntos de héroe. Derrotar a villanos, completar eventos, reclutar aliados y resolver encuentros te recompensa con puntos de héroe. Apoyar a los otros héroes, por supuesto, también te recompensará con algunos puntos de héroe.\r\nDesafío y competitivo: el juego termina después de que tú u otro héroe ganes 20 o más puntos de héroe. ¡En ese momento el héroe con más puntos de héroe es declarado ganador!\r\nFácil de aprender y muy variable: las reglas simples crean diversión para todos los fans de My Hero Academia. Las tarjetas de objetivo modulares, la colocación aleatoria de cartas y los poderes únicos de héroe fomentan las repeticiones.\r\nNúmero de jugadores y tiempo de juego promedio: este divertido juego de mesa está hecho para 2 a 4 jugadores y es adecuado para edades de 14 años en adelante. El tiempo de reproducción promedio es de aproximadamente 30 minutos.'),
(65, 'Mattel Games Juego de Cartas Nocturno Familiar UNO Dragon Ball Z', 10000, 'productos/81JjF1K6gL._AC_SY550_.jpg', 16, 5, '¡Es el clásico juego de cartas UNO que todos aman, con gráficos diseñados para los fanáticos de Dragon Ball Z! Perfecto para fanáticos del anime a partir de 7 años.\r\n​Cada tarjeta presenta gráficos de Dragon Ball Z que brindan un nuevo giro en la historia que acompaña a la tarjeta cada vez que juegas.\r\nAl igual que en el clásico juego UNO, los jugadores deben ordenar las cartas por color o número en un intento de vaciar su mano.\r\n​Incluye una tarjeta de deseos exclusiva de Wild Shenron. Al igual que otras cartas de acción, ¡puede cambiar instantáneamente el curso del juego!\r\n​UNO Dragon Ball Z es un gran regalo para coleccionistas y fanáticos del manga'),
(66, 'Topi Games One Piece - Adventure Island', 30000, 'productos/71DZx6l8yRL._AC_SY355_.jpg', 9, 5, 'Revive las aventuras de la famosa tripulación de piratas del sombrero de paja y enfrenta a los numerosos enemigos que se encuentran en tu camino para encontrar los tesoros dispersos en el Grand Line.\r\n3 modos de juego (un modo infantil, un modo de historia y un modo de juego de combate entre tripulaciones)\r\nDe 2 a 8 jugadores.\r\nA partir de 8 años de edad.\r\nConquista las islas. One Piece Adventure Island'),
(67, 'TOPI Games - Naruto Shippuden - Combate DE Ninjas - Juegos de Mesa', 30000, 'productos/71urgFOkFdL._AC_SX355_.jpg', 7, 5, 'NARUTO SHIPPUDEN: ¡Los señores feudales te necesitan para salvar el mundo Ninja! Durante la Gran Guerra, elige tu bando entre la gran Alianza de 5 países o alíate con Uchiha Madara para ayudarlo a cumplir su desastroso destino.\r\nJUEGO DE MESA: Elige el equipo de tu aldea que prefieras entre unos treinta Ninja e intenta llevar a cabo tantas misiones como sea posible de los rangos A, B, C, D y S para contrarrestar a Akatsuki.\r\nJUEGO PARA NIÑOS: Salva tantos demonios con cola como puedas y lucha contra los Ninjas de rango S solo o en equipo en Bingo Book\r\nDURACIÓN: 20 a 45 minutos\r\nEDAD: A partir de 7 años'),
(68, 'Jasco-MHA01C Juego de Cartas dedicado, Multicolor', 15000, 'productos/81TGdlhPxhL._AC_SY355_.jpg', 5, 5, 'Juego de cartas coleccionable con licencia oficial: My Hero Academia viene a la mesa. Los fanáticos de los juegos de cartas intercambiables pueden probar su (todos) poder en este tenso y estratégico juego de cartas de duelo. Como producto con licencia oficial, MHA CCG está cargado de un increíble arte de tus héroes favoritos\r\nJuego de cartas de estrategia de duelo: el juego de cartas coleccionable My Hero Academia es un juego de cartas competitivo en el que los jugadores se duelen entre sí para determinar quién es el verdadero héroe. Reúne a tus héroes, prueba contra villanos y supera a tus rivales. Construye la mejor baraja y adapta tu estrategia mientras juegas.\r\nJuego de iniciación de dos jugadores: Izuku Midoriya y Katsuko Bakugo se enfrentan en este explosivo juego de 104 cartas para principiantes para el juego de cartas coleccionable My Hero Academia. Utiliza esta baraja como un bloque de construcción en tu entrenamiento y da otro paso para convertirte en el mejor luchador UniVersus\r\nIncluye cartas raras: cada baraja de 51 cartas está lista para jugar directamente fuera de la caja y se puede ampliar con cartas de los paquetes de refuerzo My Hero Academia CCG. Estas barajas cuentan con tarjetas únicas no disponibles en paquetes de refuerzo, por lo que son necesarias para completar una colección\r\nNúmero de jugadores y tiempo de juego promedio: este divertido juego de cartas competitivo está hecho para 2 jugadores y es adecuado para edades de 14 años en adelante. El tiempo promedio de reproducción es de aproximadamente 45 minutos.'),
(69, 'WKxinxuan Llaveros de Demon Slayer', 15000, 'productos/71Ubu60cLdL._AC_SX679_.jpg', 8, 7, '【El producto contiene】: El juego de llaveros Demon Slayer contiene 12 llaveros Demon Slayer. Para evitar arañazos, la parte posterior de la figura está cubierta con una película protectora. Si ve un acabado mate, retire la película protectora en la parte posterior y Obtendrás un llavero transparente.\r\n【Resistente y no rasgado】: Los demon slayer llavero son de buena calidad, están hechos de PVC de alta calidad y ganchos de metal, son resistentes y duraderos, y son populares entre niños y adultos! La calidad es convincente, no se rompe y se puede utilizar durante mucho tiempo.\r\n【Color claro】: El color del conjunto de anime llaveros es hermoso y preciso, y los personajes de dibujos animados son claramente visibles. No hay diferencia con el color original. El tamaño de 5,5 cm también es perfecto.\r\n【Llavero exquisito】: El llavero para niños Demon Slayer se ve muy realista y convincente. Fácil de usar, también adecuado para etiquetas de llavero de espada de cazador de demonios para Navidad y Halloween.\r\n【Regalo ideal】:El llavero personalizado de Demon Slayer es un regalo para los niños! Este es el regalo perfecto para los fans de kimetsu no yaiba.Si faltan cantidades o están duplicadas, comuníquese con nosotros y le responderemos en 24 horas.'),
(70, 'Funko Pop! Keychain: One Piece - Roronoa Zoro', 5000, 'productos/61yOLgWH0L._AC_SL1200_.jpg', 12, 7, 'MINI FIGURA DE VINILO - Con una altura aproximada de 11,76 cm, esta figura de vinilo de alta calidad es un llamativo complemento para cualquier exposición o colección\r\nMATERIAL DE VINILO DE PRIMERA CALIDAD - Fabricado en vinilo de alta calidad y durabilidad, este coleccionable está hecho para durar y soportar el desgaste diario, asegurando un disfrute duradero tanto para los fans como para los coleccionistas\r\nREGALO PERFECTO PARA LOS FANS DE ONE PIECE - Ideal para fiestas, cumpleaños u ocasiones especiales y como regalo esta exclusiva figurita es un complemento imprescindible en cualquier colección de merchandising de One Piece\r\nAMPLÍA TU COLECCIÓN - Añade este exclusivo llavero de vinilo One Piece a tu creciente surtido de figuras Funko Pop! y busca otros artículos coleccionables raros y exclusivos para tener un conjunto completo\r\nVERSATILE PARTY ESSENTIALS - Utilízalos como relleno de bolsas de fiesta para niños, sorpresas para calcetines de Navidad y llamativos adornos para tartas, añadiendo un toque especial a cumpleaños y eventos.\r\nMARCA LÍDER EN CULTURA POP - Confía en la experiencia de Funko, el principal creador de artículos de cultura pop que incluye figuras de vinilo, juguetes de acción, peluches, ropa, juegos de mesa y mucho más.');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `sysapp_carrito`
--
ALTER TABLE `sysapp_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sysApp_carrito_producto_id_674a98a5_fk_sysApp_producto_id` (`producto_id`);

--
-- Indices de la tabla `sysapp_categoria`
--
ALTER TABLE `sysapp_categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sysapp_producto`
--
ALTER TABLE `sysapp_producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sysApp_producto_categoria_id_91179265_fk_sysApp_categoria_id` (`categoria_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `sysapp_carrito`
--
ALTER TABLE `sysapp_carrito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sysapp_categoria`
--
ALTER TABLE `sysapp_categoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `sysapp_producto`
--
ALTER TABLE `sysapp_producto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `sysapp_carrito`
--
ALTER TABLE `sysapp_carrito`
  ADD CONSTRAINT `sysApp_carrito_producto_id_674a98a5_fk_sysApp_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `sysapp_producto` (`id`);

--
-- Filtros para la tabla `sysapp_producto`
--
ALTER TABLE `sysapp_producto`
  ADD CONSTRAINT `sysApp_producto_categoria_id_91179265_fk_sysApp_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `sysapp_categoria` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
