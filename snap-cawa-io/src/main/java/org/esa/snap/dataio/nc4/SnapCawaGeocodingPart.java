package org.esa.snap.dataio.nc4;

import org.esa.snap.core.datamodel.*;
import org.esa.snap.core.image.ImageManager;
import org.esa.snap.core.util.StringUtils;
import org.esa.snap.dataio.netcdf.ProfileWriteContext;
import org.esa.snap.dataio.netcdf.metadata.profiles.cf.CfGeocodingPart;
import org.esa.snap.dataio.netcdf.nc.NFileWriteable;
import org.esa.snap.dataio.netcdf.nc.NVariable;
import org.esa.snap.dataio.netcdf.util.Constants;
import org.geotools.referencing.CRS;
import org.geotools.referencing.crs.DefaultGeographicCRS;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.referencing.operation.MathTransform;
import ucar.ma2.Array;
import ucar.ma2.DataType;

import java.awt.*;
import java.awt.geom.AffineTransform;
import java.io.IOException;

/**
 * todo: add comment
 * To change this template use File | Settings | File Templates.
 * Date: 26.07.2016
 * Time: 17:09
 *
 * @author olafd
 */
public class SnapCawaGeocodingPart extends CfGeocodingPart {
    public static final String TIEPOINT_COORDINATES = "tiepoint_coordinates";

    private static final int LON_INDEX = 0;
    private static final int LAT_INDEX = 1;

    @Override
    public void preEncode(ProfileWriteContext ctx, Product product) throws IOException {
        final GeoCoding geoCoding = product.getSceneGeoCoding();
        if (geoCoding == null) {
            return;
        }
        final NFileWriteable ncFile = ctx.getNetcdfFileWriteable();
                addLatLonBands(ncFile, ImageManager.getPreferredTileSize(product));
        ctx.setProperty(Constants.Y_FLIPPED_PROPERTY_NAME, false);
    }

    @Override
    public void encode(ProfileWriteContext ctx, Product product) throws IOException {
        final int h = product.getSceneRasterHeight();
        final int w = product.getSceneRasterWidth();

        final GeoCoding geoCoding = product.getSceneGeoCoding();
        final PixelPos pixelPos = new PixelPos();
        final GeoPos geoPos = new GeoPos();

        NFileWriteable ncFile = ctx.getNetcdfFileWriteable();
        NVariable latVariable = ncFile.findVariable("lat");
        NVariable lonVariable = ncFile.findVariable("lon");
        if (isGeographicCRS(geoCoding)) {
            final float[] lat = new float[h];
            final float[] lon = new float[w];
            pixelPos.x = 0 + 0.5f;
            for (int y = 0; y < h; y++) {
                pixelPos.y = y + 0.5f;
                geoCoding.getGeoPos(pixelPos, geoPos);
                lat[y] = (float) geoPos.getLat();
            }
            pixelPos.y = 0 + 0.5f;
            for (int x = 0; x < w; x++) {
                pixelPos.x = x + 0.5f;
                geoCoding.getGeoPos(pixelPos, geoPos);
                lon[x] = (float) geoPos.getLon();
            }
            latVariable.writeFully(Array.factory(lat));
            lonVariable.writeFully(Array.factory(lon));
        } else {
            final float[] lat = new float[w];
            final float[] lon = new float[w];
            final boolean isYFlipped = (Boolean) ctx.getProperty(Constants.Y_FLIPPED_PROPERTY_NAME);
            for (int y = 0; y < h; y++) {
                pixelPos.y = y + 0.5f;
                for (int x = 0; x < w; x++) {
                    pixelPos.x = x + 0.5f;
                    geoCoding.getGeoPos(pixelPos, geoPos);
                    lat[x] = (float) geoPos.getLat();
                    lon[x] = (float) geoPos.getLon();
                }
                latVariable.write(0, y, w, 1, isYFlipped, ProductData.createInstance(lat));
                lonVariable.write(0, y, w, 1, isYFlipped, ProductData.createInstance(lon));
            }
        }
    }

    private void addLatLonBands(final NFileWriteable ncFile, Dimension tileSize) throws IOException {
        final NVariable lat = ncFile.addVariable("lat", DataType.FLOAT, tileSize, "y x");
        lat.addAttribute("units", "degrees_north");
        lat.addAttribute("long_name", "latitude coordinate");
        lat.addAttribute("standard_name", "latitude");

        final NVariable lon = ncFile.addVariable("lon", DataType.FLOAT, tileSize, "y x");
        lon.addAttribute("units", "degrees_east");
        lon.addAttribute("long_name", "longitude coordinate");
        lon.addAttribute("standard_name", "longitude");
    }

    private static boolean isGeographicCRS(final GeoCoding geoCoding) {
        return (geoCoding instanceof CrsGeoCoding || geoCoding instanceof MapGeoCoding) &&
                CRS.equalsIgnoreMetadata(geoCoding.getMapCRS(), DefaultGeographicCRS.WGS84);
    }

    private void addWktAsVariable(NFileWriteable ncFile, GeoCoding geoCoding) throws IOException {
        final CoordinateReferenceSystem crs = geoCoding.getMapCRS();
        if (crs != null && crs.toWKT() != null) {
            final double[] matrix = new double[6];
            final MathTransform transform = geoCoding.getImageToMapTransform();
            if (transform instanceof AffineTransform) {
                ((AffineTransform) transform).getMatrix(matrix);
            }

            final NVariable crsVariable = ncFile.addScalarVariable("crs", DataType.INT);
            crsVariable.addAttribute("wkt", crs.toWKT());
            crsVariable.addAttribute("i2m", StringUtils.arrayToCsv(matrix));
            crsVariable.addAttribute("long_name", "Coordinate Reference System");
            final String crsCommentString = "A coordinate reference system (CRS) defines defines how the georeferenced " +
                    "spatial data relates to real locations on the Earth\'s surface";
            crsVariable.addAttribute("comment", crsCommentString);
        }
    }

}